from django import forms
from hardware.models import Condition, Category, State
from django.utils.html import conditional_escape, escape
from django.utils.encoding import force_unicode

class SelectWithTitles(forms.Select):
	def __init__(self, *args, **kwargs):
		super(SelectWithTitles, self).__init__(*args, **kwargs)
		# Ensure the titles dict exists
		self.titles = {}

	def render_option(self, selected_choices, option_value, option_label):
		title_html = (option_label in self.titles) and \
			u' title="%s" ' % escape(force_unicode(self.titles[option_label])) or ''
		option_value = force_unicode(option_value)
		selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
		return u'<option value="%s"%s%s>%s</option>' % (
			escape(option_value), title_html, selected_html,
			conditional_escape(force_unicode(option_label)))
pty_label=None
class ChoiceFieldWithTitles(forms.ChoiceField):
	widget = SelectWithTitles

	def __init__(self, choices=(), *args, **kwargs):
		choice_pairs = [(c[0], c[1]) for c in choices]
		super(ChoiceFieldWithTitles, self).__init__(choices=choice_pairs, *args, **kwargs)
		self.widget.titles = dict([(c[1], c[2]) for c in choices])

class HardwareForm(forms.Form):
	lendlengthtypes = (
		('1', 'Tag(e)'),
		('7', 'Woche(n)'),
		('30', 'Monat(e)'),
		('356', 'Jahr(e)')
	)
	error_css_class = 'error'
	name = forms.CharField(max_length=200)
	description = forms.CharField(widget=forms.Textarea)
	condition = forms.ModelChoiceField(queryset=Condition.objects.all(), empty_label=None)
	category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
	state = ChoiceFieldWithTitles()
	lendlength = forms.IntegerField(required=False)
	lendlengthtype = forms.ChoiceField(choices=lendlengthtypes, required=False)

	ownlocation = forms.BooleanField(required=False)
	city = forms.CharField(max_length=200, required=False)
	postcode = forms.CharField(max_length=5, required=False)
	street = forms.CharField(max_length=200, required=False)


	def __init__(self, *args, **kwargs):
		super(HardwareForm, self).__init__(*args, **kwargs)   

		choices = []
		for c in State.objects.all():
			choices.append((c.id, c.name, c.temporary))
		self.fields['state'] = ChoiceFieldWithTitles(choices = choices)


class SendmailForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea)

class SimpleSearchForm(forms.Form):
	searchquery = forms.CharField(required=False)

class SearchForm(SimpleSearchForm):
	SORT_BY_CHOICES = (
		("", "Sortiere nach"),
		("name", "Name"),
		("owner", "Besitzer"),
		("condition", "Zustand"),
		("category", "Kategorie"),
		("state", "Art")
	)
	error_css_class = 'error'

	condition = forms.ModelChoiceField(queryset=Condition.objects.all(), empty_label="Zustand", required=False, widget=forms.Select(attrs={"class":"input-medium",}))
	category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Kategorie", required=False, widget=forms.Select(attrs={"class":"input-medium",}))
	state = forms.ModelChoiceField(queryset=State.objects.all(), empty_label="Art", required=False, widget=forms.Select(attrs={"class":"input-medium",}))
	sortby = forms.ChoiceField(choices=SORT_BY_CHOICES, required=False, widget=forms.Select(attrs={"class":"input-medium",}))

class LendForm(forms.Form):
	username = forms.CharField()