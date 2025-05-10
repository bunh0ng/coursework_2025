import telebot
from telebot import types
from config import bot_settings
from commands.start import start
from commands.search import search_record, search_type, search_table, search_query
from commands.add_record import add_record, data_input, table_selection
from commands.delete_record import delete_record, delete_data
from commands.return_back import return_back
from commands.show_invoices import show_invoices, ask_period
from commands.check_fill import checkfill
from commands.most_valuable_customers import mv_customers
from commands.most_sold_parts import ms_parts 
from commands.most_valuable_employee import mv_employee
from commands.most_active_suppliers import ma_suppliers
from commands.graphics.graphic import graphic_types, plot_selection
