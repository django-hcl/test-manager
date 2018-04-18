from django import template

register = template.Library()


@register.filter()
def duplicate(sectionnamee, duplicate_list):
     is_duplicate = False
     for value in duplicate_list:
         if value['section_name'] == sectionnamee.section_name:
             is_duplicate = True
             break
     if is_duplicate:
         return sectionnamee.section_name + sectionnamee.section_description
     else:
         return sectionnamee.section_name