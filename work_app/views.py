from django.shortcuts import render
from .models import *
from .forms import OrderCreateForm, OrderEditForm
from datetime import date, datetime, timedelta
from django.forms.models import model_to_dict


def timer(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        print('function: ', func.__repr__(), 'duration: ', end - start)
        return result

    return wrapper


def home(request):
    return render(request, 'work_app/home.html')


# Визначення, чи є вільна кровать у заданій кімнаті в заданому відрізку часу
def is_free_place(room, date_start, date_stop):
    capacity = Room.objects.get(room=room).capacity
    found_orders = 0
    select_orders_by_room = Order.objects.get(order_room=room)
    for order in select_orders_by_room:
        if order.date_start <= date_start and order.date_stop >= date_stop:
            found_orders += 1
    return found_orders < capacity


def is_bed_free_at_day(bed_id, day_start=date.today()):
    required_moment = day_start
    orders = Order.objects.filter(order_bed_id=bed_id)
    wanted = orders.filter(date_start__lte=required_moment) & orders.filter(date_stop__gte=required_moment)
    return bool(len(wanted))


@timer
def current_bed_map():
    all_rooms = Room.objects.all()
    map_of_hostel = []
    for room in all_rooms:
        beds_in_room = []
        for bed in range(1, room.capacity + 1):
            bed_in_room = Bed.objects.filter(bed_room__id=room.id).get(number=bed).id
            beds_in_room.append(is_bed_free_at_day(bed_in_room))
        map_of_hostel.append(beds_in_room)
    return map_of_hostel


@timer
def take_month_matrix(start_date):
    interval = 28
    start_date -= timedelta(int(interval / 2) - 1)
    # на входе дата в формате date (не в datetime!)

    date_days = [(start_date + timedelta(i)).day for i in range(interval)]
    #
    week = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
    week_days = (week[start_date.weekday():] + week * 5)[:interval]
    line_blank = []
    for i in range(interval):
        if week_days[i] in ['сб', 'вс']:
            line_blank.append(['free_w', 'none'])
        else:
            line_blank.append(['free__', 'none'])

    matrix = []
    beds = list(Bed.objects.all().values_list())
    for bed in beds:
        get_bed_orders = Order.objects.filter(order_bed_id=bed[0],
                                              date_start__lte=start_date + timedelta(interval - 1),
                                              date_stop__gte=start_date)
        if bed[2] == 1:
            matrix.append(['комната ' + str(bed[1])])

        line = line_blank[:]

        for order in get_bed_orders:
            left = (order.date_start - start_date).days if (order.date_start - start_date).days > -1 else 0
            right = \
                (order.date_stop - start_date).days if (order.date_stop - start_date).days < interval else interval - 1

            if date.today() > order.date_stop:
                color = 'past__'
            elif date.today() < order.date_start:
                color = 'future'
            else:
                color = 'actual'

            if order.order_client_id == 9999:
                color = 'repair'

            for i in range(right - left + 1):
                line[left + i] = [color, order.id]

        matrix.append([bed[2], line])

    # строка названия месяца/месяцев. если для названия мало места (1-2 дня попадает) то пустая строка
    month_line = []
    colspan = 1
    month_names = ['', 'январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
                   'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
    for i in range(interval):
        if (start_date + timedelta(i + 1)).day == 1 or i == interval - 1:
            month = month_names[(start_date + timedelta(i)).month] if colspan > 1 else ''
            month_line.append([month, colspan])
            colspan = 1
        else:
            colspan += 1

    return matrix, date_days, week_days, month_line, int(interval / 2)


@timer
def get_more_tables(request):
    return show_front_desk_table(request, request.GET.get('dateText'))


def show_front_desk_table(request, start_date):
    matrix, date_days, week_days, month_line, half_interval = take_month_matrix(
        datetime.strptime(start_date, '%d.%m.%Y').date())

    return render(request, 'work_app/_table_front_desk.html', context={'matrix': matrix,
                                                                       'date_days': date_days,
                                                                       'week_days': week_days,
                                                                       'month_line': month_line,
                                                                       'half_interval': half_interval,
                                                                       'start_date': start_date})


@timer
def get_order_form(request):
    print('________')

    if request.method == 'POST':

        return show_front_desk_table(request, request.POST.get('dataText'))

    if request.method == 'GET':
        raw_cell_date = request.GET.get('cell_date')
        cell_date = datetime.strptime(raw_cell_date, '%d.%m.%Y').date()
        order_number = request.GET.get('order_number_class').split('_')[1]

        if order_number == 'none':
            # create new order
            order_form = OrderCreateForm(data={'date_start': cell_date})
            print('order_form data:')
            for field in order_form:
                print(field.name, '_____________', field)

            return render(request, 'work_app/_order_form.html', context={'cell_date': raw_cell_date,
                                                                         'order_form': order_form})

        else:
            # edit existing order
            order_from_base_dict = model_to_dict(Order.objects.get(id=order_number))
            order_form = OrderEditForm(data=order_from_base_dict, initial=order_from_base_dict)
            print('is valid: ', order_form.is_valid())
            print('errors: ', order_form.errors)

            return render(request, 'work_app/_order_form.html', context={'cell_date': raw_cell_date,
                                                                         # 'order': order_number,
                                                                         'order_form': order_form})

    return
