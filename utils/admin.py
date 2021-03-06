# Import regex, json, os and logging modules from standard library
import sys, os, re, importlib, fileinput, codecs

# Import modules from python-telegram-bot
from telegram import (ParseMode, InlineKeyboardButton, InlineKeyboardMarkup)

import utils.get_strings

from utils.get_strings import get_strings as _

import utils.utils
from utils.utils import send_typing_action, user_is_admin, build_menu, restricted

from utils.admin_data import admin_menu_data as menu_data
import settings.settings as settings
import utils.user_menu

main = importlib.import_module('od-telegram-bot')

CHECK_ACCESS_CODE, CHECK_ANSWER, ADMIN_TOOLS = range(3)



@restricted
def admin_settings(update,context):
    context.chat_data['menu_log'] = ['start']
    context.chat_data['current_menu_step'] = 'start'
    show_inline_menu(update, context, 'input')
    return ADMIN_TOOLS

@restricted
def show_inline_menu(update, context, before, success_message = None):
    query = update.callback_query
    current_menu_step = context.chat_data['current_menu_step']

    button_list = [InlineKeyboardButton(button, callback_data=idx) for idx, button in enumerate(menu_data[current_menu_step]['answers'])]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))

    to_append = ''

    if current_menu_step == 'edit_messages':
        # For convenience the messages are directly loaded from the according lang file

        lang_file = f'locale/{settings.LANG}-default.py'
        # Pattern to match variable names in the lang file
        re_pattern = fr'^\s*([a-z|_]*)\s*='
        messages = []

        # Open the lang file
        lines = []
        with codecs.open(lang_file, 'r', encoding='utf-8') as fi:
            for line in fi:
                lines.append(line)

        for idx, line in enumerate(lines):
            # If a variable is found
            match = re.search(re_pattern, line)
            if match:
                # List with the message name
                single_message = [match.group(1)]
                # Get the comment in the line before
                comment = lines[idx-1]
                # Split the name and the description of the variable
                description = [i.strip().replace('#', '') for i in comment.split('-')]
                # Append the name and description to the message
                single_message += description
                messages.append(single_message)

        button_list = [InlineKeyboardButton(single_message[1], callback_data=idx) for idx, single_message in enumerate(messages)]
        len_button_list = len(button_list)
        button_list.append(InlineKeyboardButton(_('back_button'), callback_data=len_button_list))
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
        to_append += f'\nPlease note, that you will set custom messages for the currently selected language {settings.LANG}.\n'
        context.chat_data['messages'] = messages

    elif current_menu_step == 'edit_single_message':
        messages = context.chat_data['messages']
        single_message_index = context.chat_data['single_message_index']
        single_message = messages[single_message_index]
        to_append += f'Message: {single_message[1]}\nLanguage: {settings.LANG}\nDescription: {single_message[2]}\n'
        to_append += f'The current value is: {_(single_message[0])}'


    if menu_data[current_menu_step]['type'] == 'input':
        to_append += '\nWrite X to delete the value.'

    if before == 'input':
        message = success_message if success_message else ""
        message += menu_data[current_menu_step]['text']
        message += to_append
        update.message.reply_text(message, reply_markup=reply_markup)

    elif before == 'menu':
        message = menu_data[current_menu_step]['text']
        message += to_append
        query.edit_message_text(text=message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)


@restricted
# Entry point if the admin used the menu
def check_query(update, context):
    query = update.callback_query
    query.answer()
    answer = int(query.data)

    current_menu_step = context.chat_data['current_menu_step']

    if current_menu_step == 'edit_messages':
        len_button_list = len(context.chat_data['messages'])
        if answer == len_button_list:
            answer = 0
        else:
            context.chat_data['menu_log'].append(current_menu_step)
            context.chat_data['single_message_index'] = answer
            context.chat_data['current_menu_step'] = 'edit_single_message'
            return show_inline_menu(update, context, 'menu')

    context.chat_data['menu_log'].append(current_menu_step)

    if menu_data[current_menu_step]['type'] == 'select':
        current_menu_step = menu_data[current_menu_step]['logic'][answer]

        if current_menu_step == 'back':
            current_menu_step = context.chat_data['menu_log'][-2]
            context.chat_data['menu_log'][:2]

        elif current_menu_step == 'exit_settings':
            query.edit_message_reply_markup(None)
            context.chat_data['menu_log'] = ['start']
            context.chat_data['current_menu_step'] = 'start'
            return utils.user_menu.show_inline_menu(update, context, 'menu')


    # If admin was supposed to make an input but used the buttons instead
    # also if user used back button
    elif menu_data[current_menu_step]['type'] == 'input':
        log = context.chat_data['menu_log']
        try:
            if menu_data[current_menu_step]['logic'][answer] == 'input_back':
                current_menu_step = context.chat_data['menu_log'][-2]
                context.chat_data['menu_log'][:2]
            else:
                raise IndexError('')
        except IndexError:
            # Go back until the last select menu is found
            for i in reversed(range(len(log))):
                old_step = [i]
                if menu_data[old_step]['type'] == 'select':
                    current_menu_step = old_step
                    context.chat_data['menu_log'][:i]
                    break
    context.chat_data['current_menu_step'] = current_menu_step
    show_inline_menu(update, context, 'menu')

@restricted
# Entry point if the admin sent a new value for a setting
def check_input(update, context):
    current_menu_step = context.chat_data['current_menu_step']

    # Only react if user was asked to make an input
    if 'value' in menu_data[current_menu_step]:
        success_message = menu_data[current_menu_step].get('success', '')

        new_value = update.message.text.strip()
        if new_value == 'X':
            if current_menu_step == 'available_queries':
                new_value = []
            else:
                new_value = ''


        if menu_data[current_menu_step]['value'] == 'env':
            if (current_menu_step == 'edit_image') and (new_value != ''):
                valid_url = utils.utils.test_image(new_value)
                if(not valid_url):
                    return show_inline_menu(update, context, 'input', 'Invalid Image URL\n')

            if (current_menu_step == 'available_queries') and (new_value != '') and (new_value != []):
                temp_value = new_value.splitlines()
                new_value = []
                for idx, e in enumerate(temp_value):
                    list = [i.strip() for i in e.split('-')]
                    if re.match("^[a-z]{10}$", list[1]):
                        new_value.append(list)
                    else:
                        return show_inline_menu(update, context, 'input', f'The access code in line {idx+1} is invalid. Please correct the mistake and send me the list again. \n')


        # Open settings file and set new var
            var = menu_data[current_menu_step]['var']
            settings_file = 'settings/custom_settings.py'
            re_pattern = fr'^{var}.*$'
            new_entry = f"{var} = '{new_value}'" if current_menu_step != 'available_queries' else f"{var} = {new_value}"
            var_exists = False

            tmp_name = 'tmp.py'

            with codecs.open(settings_file, 'r', encoding='utf-8') as fi, \
                codecs.open(tmp_name, 'w', encoding='utf-8') as fo:

                # If message var exists overwrite it
                for line in fi:
                    if re.match(re_pattern, line):
                        var_exists = True
                        new_line = re.sub(re_pattern, new_entry, line)
                    else:
                        new_line = line
                    fo.write(new_line)

                if not var_exists:
                    fo.write('\n')
                    fo.write(new_entry)

            os.rename(settings_file, 'admin_settings_bak') # rename original
            os.rename(tmp_name, settings_file) # rename temp to original name

            if var_exists:
                reload_settings()
                if current_menu_step != 'available_queries':
                    success_message += "\n" + getattr(settings, var) + "\n"

        elif menu_data[current_menu_step]['value'] == 'message':

        # Open message files and set new var
            messages = context.chat_data['messages']
            single_message_index = context.chat_data['single_message_index']
            single_message = single_message = messages[single_message_index]

            var = single_message[0]
            lang_file = f'locale/{settings.LANG}.py'
            re_pattern = rf'^{var}.*$'
            new_entry = f"{var} = '{new_value}'"
            var_exists = False

            tmp_name = 'tmp.py'

            with codecs.open(lang_file, 'r', encoding='utf-8') as fi, \
                codecs.open(tmp_name, 'w', encoding='utf-8') as fo:

                # If message var exists overwrite it
                for line in fi:
                    if re.match(re_pattern, line):
                        var_exists = True
                        new_line = re.sub(re_pattern, new_entry, line)
                    else:
                        new_line = line
                    fo.write(new_line)

                if not var_exists:
                    fo.write('\n')
                    fo.write(new_entry)

            os.rename(lang_file, lang_file + '_bak') # rename original
            os.rename(tmp_name, lang_file) # rename temp to original name

            reload_settings()
            success_message += f"Very well, Sir. I set {single_message[1]} to: \n{_(var)}\n"
            current_menu_step = 'edit_messages'

    # Send 'success' with according keyboard above
        current_menu_step = context.chat_data['menu_log'][-1]
        context.chat_data['menu_log'].pop()
        context.chat_data['current_menu_step'] = current_menu_step
        return show_inline_menu(update, context, 'input', success_message)

def reload_settings():
    settings.reload_settings()
    utils.get_strings.reload_messages()
    importlib.reload(settings)
    utils.utils.reload_settings()
    utils.user_menu.reload_settings()
    main.reload_settings()
