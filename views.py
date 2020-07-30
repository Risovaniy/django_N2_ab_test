from collections import Counter

from django.shortcuts import render_to_response

counter_show = Counter({'orig': 0, 'test': 0})
counter_click = Counter({'orig': 0, 'test': 0})


def index(request):
    are_you_from = request.GET.get('from-landing')
    if are_you_from == 'original':
        counter_click.update(['orig'])
    elif are_you_from == 'test':
        counter_click.update(['test'])
    return render_to_response('index.html')


def landing(request):
    if request.GET.get('ab-test-arg') == 'test':
        counter_show.update(['test'])
        return render_to_response('landing_alternate.html')
    counter_show.update(['orig'])
    return render_to_response('landing.html')


def stats(request):
    try:
        conversion_orig = counter_click['orig'] / counter_show['orig']
        conversion_test = counter_click['test'] / counter_show['test']
    except ZeroDivisionError:
        conversion_test = conversion_orig = 'Ошибка! Один из лендингов ни разу не был показан!'
    return render_to_response('stats.html', context={
        'test_conversion': conversion_orig,
        'original_conversion': conversion_test,
    })
