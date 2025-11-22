from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Filtro para acceder a items de diccionarios en templates
    Uso: {{ estado_actual|get_item:alumno.id }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter(name='addclass')
def addclass(field, css_class):
    """
    Añade clases CSS a campos de formulario
    Uso: {{ form.field|addclass:"form-control" }}
    """
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='format_time')
def format_time(time_obj):
    """
    Formatea objetos time al formato HH:MM
    Uso: {{ asistencia.hora_ingreso|format_time }}
    """
    if time_obj:
        return time_obj.strftime('%H:%M')
    return '-'

@register.filter(name='format_date')
def format_date(date_obj):
    """
    Formatea objetos date al formato DD/MM/YYYY
    Uso: {{ asistencia.fecha|format_date }}
    """
    if date_obj:
        return date_obj.strftime('%d/%m/%Y')
    return '-'

@register.filter(name='estado_color')
def estado_color(estado):
    """
    Devuelve una clase CSS según el estado de asistencia
    Uso: {{ asistencia.estado|estado_color }}
    """
    colores = {
        'Presente': 'success',
        'Ausente': 'danger',
        'Retirado': 'warning'
    }
    return colores.get(estado, 'secondary')

@register.filter(name='estado_icon')
def estado_icon(estado):
    """
    Devuelve un icono según el estado de asistencia
    Uso: {{ asistencia.estado|estado_icon }}
    """
    iconos = {
        'Presente': '✓',
        'Ausente': '✗',
        'Retirado': '→'
    }
    return iconos.get(estado, '?')

@register.filter(name='porcentaje')
def porcentaje(valor, total):
    """
    Calcula el porcentaje
    Uso: {{ presentes|porcentaje:total_alumnos }}
    """
    try:
        if total > 0:
            return round((valor / total) * 100, 1)
        return 0
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter(name='multiply')
def multiply(value, arg):
    """
    Multiplica dos valores
    Uso: {{ dias|multiply:alumnos }}
    """
    try:
        return value * arg
    except (ValueError, TypeError):
        return 0