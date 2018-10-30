# -*- coding: utf8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from django.shortcuts import get_object_or_404, redirect
from django.utils.http import is_safe_url
from django.core.urlresolvers import reverse
from django import forms
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.db.models import Q
from django.conf import settings

from urlparse import urlparse

import sorl

from account.mixins import LoginRequiredMixin

from .models import Schedule, Speaker, OrganiserType, Presentation, Attendee, StandingCommittee
from .forms import AttendeeForm
from blocks.models import Block


class ScheduleMixin(object):
    """
    A view mixin to retrieve the related schedule for other views,
    force logins for private schedules and objects related to
    private schedules, and automatically filter objects to those
    related to the given schedule.
    """

    # Override this if your url uses a different kwarg name for
    # the schedule's slug
    schedule_slug_kwarg = 'schedule_slug'

    def dispatch(self, request, *args, **kwargs):
        """
        Overridden dispatch so that self.schedule is available
        throughout the whole method chain of any view.
        """
        self.schedule = get_object_or_404(
            Schedule,
            slug=kwargs.get(self.schedule_slug_kwarg)
        )
        if self.schedule.private and not request.user.is_authenticated():
            return redirect('%s?next=%s' % (reverse('account_login'), request.path))
        return super(ScheduleMixin, self).dispatch(request, *args, **kwargs)

    # def get_queryset(self):
    #     """
    #     Overridden get_queryset to filter the models down to those
    #     that are related to this schedule.
    #     """
    #     return super(ScheduleMixin, self).get_queryset().filter(schedule=self.schedule)

    def get_context_data(self, **kwargs):
        context = super(ScheduleMixin, self).get_context_data(**kwargs)
        context['schedule'] = self.schedule
        return context


class ScheduleView(DetailView):
    model = Schedule
    context_object_name = 'schedule'

    def get(self, request, *args, **kwargs):
        """
        Overridden get from BaseDetailView in order to check the
        schedule access before rendering the view.
        """
        self.object = self.get_object()

        if self.object.private and not request.user.is_authenticated():
            return redirect('%s?next=%s' % (reverse('account_login'), request.path))

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)

        context['days'] = {}

        slots = context['schedule'].slots.order_by('start')

        for slot in slots:
            if slot.start.date() not in context['days']:
                context['days'][slot.start.date()] = []
            context['days'][slot.start.date()].append(slot)

        sidebar_block = Block.objects.get(slug="{}-sidebar".format(context['schedule'].slug))
        context['sidebar_block'] = sidebar_block.content
        try:
            footer_block = Block.objects.get(slug="{}-footer".format(context['schedule'].slug))
            context['footer_block'] = footer_block.content
        except Block.DoesNotExist:
            context['footer_block'] = None
        return context


class Schedule2017SummaryView(TemplateView):
    template_name = 'ainow/2017-summary.html'

    def get_context_data(self, **kwargs):

        context = super(Schedule2017SummaryView, self).get_context_data(**kwargs)

        context['schedule'] = Schedule.objects.get(slug='2017')

        return context


class ScheduleTaipeiSummaryView(TemplateView):
    template_name = 'ainow/taipei-summary.html'

    def get_context_data(self, **kwargs):

        context = super(ScheduleTaipeiSummaryView, self).get_context_data(**kwargs)

        context['schedule'] = Schedule.objects.get(slug='taipei')

        return context


class Schedule2018SummaryView(TemplateView):
    template_name = 'ainow/2018-summary.html'

    def get_context_data(self, **kwargs):

        context = super(Schedule2018SummaryView, self).get_context_data(**kwargs)

        context['schedule'] = Schedule.objects.get(slug='2018')

        return context

class Schedule2019SummaryView(TemplateView):
    template_name = 'ainow/2019-summary.html'

    def get_context_data(self, **kwargs):

        context = super(Schedule2019SummaryView, self).get_context_data(**kwargs)

        context['schedule'] = Schedule.objects.get(slug='2019')

        return context


class SponsorshipView(TemplateView):
    template_name = 'ainow/sponsorship.html'

    def get_context_data(self, **kwargs):

        context = super(SponsorshipView, self).get_context_data(**kwargs)

        context['schedule'] = Schedule.objects.get(slug=settings.CONFERENCE_DEFAULT_SCHEDULE)

        return context


class LocalView(TemplateView):
    template_name = 'ainow/local.html'

    def get_context_data(self, **kwargs):

        context = super(LocalView, self).get_context_data(**kwargs)

        context['schedule'] = Schedule.objects.get(slug=settings.CONFERENCE_DEFAULT_SCHEDULE)

        context['sessions'] = [{
            "kind": "other",
            "start": "09:00",
            "name": "Conference registration & refreshments",
        }, {
            "kind": "talk",
            "start": "10:00",
            "presentations": [{
                "title": "Welcome to TICTeC Local",
                "speakers": [{
                    "name": "Mark Cridge",
                    "role": "Chief Executive",
                    "organisation": "mySociety",
                }]
            }]
        }, {
            "kind": "talk",
            "start": "10:10",
            "presentations": [{
                "title": "Civic Tech and Local Gov: the evidence base",
                "short_description": "The research on Civic Tech at the local level shows us what’s already working — and provides ample inspiration for new initiatives.",
                "speakers": [{
                    "name": "Dr Rebecca Rumbul",
                    "role": "Head of Research",
                    "organisation": "mySociety",
                }]
            }]
        }, {
            "kind": "keynote",
            "start": "10:20",
            "presentations": [{
                "title": "Opening keynote: Fixing the plumbing",
                "short_description": "MHCLG will share how they are helping Local Government to ‘fix the plumbing’, by putting the basics in place now — and quickly.",
                "speakers": [{
                    "name": "Paul Maltby",
                    "role": "Chief Digital Officer",
                    "organisation": "Ministry of Housing, Communities & Local Government",
                }]
            }]
        }, {
            "kind": "talk",
            "start": "10:40",
            "presentations": [{
                "title": "Introducing Public Square",
                "short_description": "Citizen participation is often low, but the desire to get things changed is rising. Public Square will explore how to increase democratic engagement beyond elections.",
                "speakers": [{
                    "name": "Michelle Brook",
                    "organisation": "Democratic Society",
                }, {
                    "name": "Mel Stevens",
                    "organisation": "Democratic Society",
                }]
            }]
        }, {
            "kind": "other",
            "start": "11:00",
            "name": "Refreshment break",
        }, {
            "kind": "talk",
            "start": "11:20",
            "presentations": [{
                "title": "Where Civic Tech meets Local Government",
                "short_description": "Inspiring projects that are showing results — across a broad range of policy areas.",
                "speakers": [{
                    "name": "Andrea Bowes",
                    "role": "Data and Information Systems Technical Architect",
                    "organisation": "Lincolnshire County Council",
                }, {
                    "name": "Zara Rahman",
                    "role": "Research, Engagement and Communities Team Lead",
                    "organisation": "The Engine Room",
                }, {
                    "name": "Beatrice Karol Burks and Elle Tweedy",
                    "organisation": "Futuregov",
                }, {
                    "name": "Sarah Drummond",
                    "role": "Co-founder and MD",
                    "organisation": "Snook",
                }, {
                    "name": "Julian Tait and Jamie Whyte",
                    "organisation": "Open Data Manchester",
                }, {
                    "name": "Helen Gerling",
                    "role": "Director of Consultancy",
                    "organisation": "Shaping Cloud",
                }, {
                    "name": "Tayo Medupin",
                    "role": "Innovation Director",
                    "organisation": "Shift",
                }]
            }]
        }, {
            "kind": "other",
            "start": "12:40",
            "name": "Lunch",
        }, {
            "kind": "talk",
            "start": "13:40",
            "presentations": [{
                "title": "The citizen shift",
                "short_description": "Democracy needs a helping hand. How can we promote the role of the citizen and encourage better participation in society?",
                "speakers": [{
                    "name": "Jon Alexander",
                    "role": "Founding Partner",
                    "organisation": "New Citizenship Project",
                }]
            }]
        }, {
            "kind": "talk",
            "start": "14:00",
            "presentations": [{
                "title": "Panel discussion: Reaching the furthest first",
                "short_description": "Decisions made at the local level can have an impact on the opportunities, living standards, health and happiness of thousands of people. We hear from panellists who are putting ethical considerations at the forefront.",
                "speakers": [{
                    "name": "Eddie Copeland",
                    "role": "Director of Government Innovation",
                    "organisation": "Nesta",
                }, {
                    "name": "Beatrice Karol Burks",
                    "role": "Studio Director",
                    "organisation": "Futuregov",
                }, {
                    "name": "Dr Eloise Elliott-Taysom",
                    "role": "Product Lead",
                    "organisation": "IF",
                }, {
                    "name": "Nick Stanhope",
                    "role": "Founder and CEO",
                    "organisation": "Shift",
                }, {
                    "name": "Steve Skelton",
                    "role": "Strategic Head: Policy & Information Services",
                    "organisation": "Stockport Council",
                }]
            }]
        }, {
            "kind": "talk",
            "start": "14:40",
            "presentations": [{
                "title": "The Consul project for citizen participation",
                "short_description": "Consul’s participation software is used by 90 governments in 18 different countries, giving citizens a voice in decisions about their own neighbourhoods. Jose highlights experiences within Madrid City Council as well as the global impact of Consul.",
                "speakers": [{
                    "name": "José María Becerra González",
                    "organisation": "Consul Project at Madrid City Council",
                }]
            }]
        }, {
            "kind": "other",
            "start": "15:00",
            "name": "Refreshment break",
        }, {
            "kind": "talk",
            "start": "15:15",
            "presentations": [{
                "title": "Panel discussion: Citizens or customers",
                "short_description": "The way a council talks about its residents can reveal a lot about their ethos. Can we reshape the government-to-citizen relationship for the good of all?",
                "speakers": [{
                    "name": "Miranda Marcus",
                    "role": "Research and Development Programme Lead",
                    "organisation": "The Open Data Institute",
                }, {
                    "name": "Jose Maria Becerra Gonzalez",
                    "role": "Consul Project",
                    "organisation": "Madrid City Council",
                }, {
                    "name": "Jon Alexander",
                    "role": "Founding Partner",
                    "organisation": "New Citizenship Project",
                }, {
                    "name": "Carl Whistlecraft",
                    "role": "Head of Democracy",
                    "organisation": "Kirklees Council",
                }, {
                    "name": "Sarah Drummond",
                    "role": "Co-founder and MD",
                    "organisation": "Snook",
                }]
            }]
        }, {
            "kind": "keynote",
            "start": "15:55",
            "presentations": [{
                "title": "Closing keynote: The Deal",
                "short_description": "Wigan are trying something new: a contract between residents and the council as both sides strive for a better borough. Alison shares the lessons and impacts so far.",
                "speakers": [{
                    "name": "Alison McKenzie-Folan",
                    "role": "Deputy CEO and Digital Transformation Lead",
                    "organisation": "Wigan Council"
                }]
            }]
        }, {
            "kind": "talk",
            "start": "16:15",
            "presentations": [{
                "title": "Panel discussion: Making it happen",
                "short_description": "Today’s all about inspiring ideas — but how are we going to get them implemented? Hear from the decision makers about what it’ll take to put things in motion.",
                "speakers": [{
                    "name": "Emer Coleman",
                    "role": "Digital Leader",
                    "organisation": "The Federation",
                }, {
                    "name": "Paul Maltby",
                    "role": "CDO",
                    "organisation": "Ministry of Housing, Communities & Local Government",
                }, {
                    "name": "Alison McKenzie-Folan",
                    "role": "Deputy CEO and Digital Transformation Lead",
                    "organisation": "Wigan Council",
                }, {
                    "name": "Theo Blackwell",
                    "organisation": "Chief Digital Officer for London",
                }, {
                    "name": "Phil Swan",
                    "role": "Chief Information Officer",
                    "organisation": "Greater Manchester Combined Authority",
                }, {
                    "tbc": True,
                }]
            }]
        }, {
            "kind": "talk",
            "start": "16:55",
            "presentations": [{
                "title": "Wrap up",
                "short_description": "Summing up and reflection on the day’s events and what we’ve learned.",
                "speakers": [{
                    "name": "Linda O’Halloran",
                    "role": "Head of Local Digital Collaboration Unit",
                    "organisation": "Ministry of Housing, Communities & Local Government",
                }]
            }]
        }, {
            "kind": "other",
            "start": "17:00",
            "name": "Finish",
        }]

        return context


class SpeakerListView(ScheduleMixin, ListView):
    model = Speaker
    context_object_name = 'speakers'

    def get_queryset(self):
        """
        Speakers are linked to a schedule by their presentation(s) slot(s).
        """

        return Speaker.objects.filter(
            Q(presentations__session__slot__schedule=self.schedule)
        ).order_by('name').distinct()


class Schedule2018SpeakerListView(SpeakerListView):
    template_name = 'conference/2018-speaker_list.html'

    def get_context_data(self, **kwargs):

        context = super(Schedule2018SpeakerListView, self).get_context_data(**kwargs)

        context['keynotespeakers'] = [
            Speaker.objects.filter(slug='martha-lane-fox').get(),
            Speaker.objects.filter(slug='jonathan-fox').get()
        ]

        return context


class SpeakerView(ScheduleMixin, DetailView):
    model = Speaker
    context_object_name = 'speaker'

    def get_queryset(self):
        """
        Speakers are linked to a schedule by their presentation(s) slot(s).
        """
        return Speaker.objects.filter(
            Q(presentations__session__slot__schedule=self.schedule)
        ).distinct()

    def get_context_data(self, **kwargs):

        context = super(SpeakerView, self).get_context_data(**kwargs)

        context['presentations'] = context['speaker'].presentations.filter(
            Q(session__slot__schedule=self.schedule)
        )

        return context


class OrganiserTypeListView(ScheduleMixin, ListView):
    model = OrganiserType
    context_object_name = 'organiser_types'

    def get_queryset(self):
        return OrganiserType.objects.all()


class StandingCommitteeListView(ListView):
    model = StandingCommittee
    context_object_name = 'standing_committee'


class PresentationView(ScheduleMixin, DetailView):
    model = Presentation
    context_object_name = 'presentation'

    def get_context_data(self, **kwargs):
        context = super(PresentationView, self).get_context_data(**kwargs)
        if context['presentation'].prezi_link:

            parsed = urlparse(context['presentation'].prezi_link)
            context['prezi_embed_slug'] = parsed.path.split("/")[1]
        return context


class PresentationListView(ListView):
    model = Presentation
    context_object_name = 'presentations'

    def get_context_data(self, **kwargs):
        context = super(PresentationListView, self).get_context_data(**kwargs)
        context['schedule'] = Schedule.objects.get(slug='2017')
        # This is very hacky, but we want to show both sets of talks, and
        # they're not easily differentiated at this stage
        workshop_slugs = [
            'ai-now-overview-and-introduction',
            'time-different-opportunities-and-challenges-artifi',
            'great-decoupling',
            'uncovering-machine-bias',
            'labor-makes-ai-magic',
            'time-different-race-labor-and-ai',
            'symbiotic-human-robot-interaction',
            'bending-gig-economy-toward-equity',
            'who-gets-think-about-ai',
            'machining-ethics',
            'elevating-human-condition-through-new-partnership',
            'machine-learning-and-healthcare-risks-and-rewards',
            'sites-deliberation',
            'complementary-vs-substitutive-automation-healthcar',
            'we-classified'
        ]
        symposium_slugs = [
            'welcome-ai-now',
            'introductions-ed-felten',
            'conversation-white-house-past-and-present',
            'three-questions-three-tech-leaders',
            'plenary-panel-inequality-labor-health-and-ethics-a'
        ]
        context['workshop_presentations'] = []
        for slug in workshop_slugs:
            context['workshop_presentations'].append(Presentation.objects.get(slug=slug))

        context['symposium_presentations'] = []
        for slug in symposium_slugs:
            context['symposium_presentations'].append(Presentation.objects.get(slug=slug))

        return context


class AttendeeListView(ScheduleMixin, ListView):
    model = Attendee
    context_object_name = 'attendees'

    def get_queryset(self):
        """
        Speakers are linked to a schedule by their presentation(s) slot(s).
        """
        return Attendee.objects.filter(
            Q(schedules=self.schedule)
        ).distinct()


class AttendeeView(ScheduleMixin, DetailView):
    model = Attendee
    context_object_name = 'attendee'


class AttendeeCreateUpdateView(LoginRequiredMixin,
                               SingleObjectTemplateResponseMixin,
                               ModelFormMixin,
                               ProcessFormView):
    """A combined create and update view for Attendees"""
    # Taken from http://stackoverflow.com/a/30948175
    model = Attendee
    context_object_name = 'attendee'
    template_name = 'conference/attendee_profile_form.html'
    form_class = AttendeeForm
    success_url = '/profile/'  # Come back to this page

    def dispatch(self, request, *args, **kwargs):
        self.schedule = Schedule.objects.get(slug=settings.CONFERENCE_DEFAULT_SCHEDULE)
        return super(AttendeeCreateUpdateView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return self.request.user.conference_attendee_profile
        except AttributeError:
            return None

    def get_initial(self):
        initial = super(AttendeeCreateUpdateView, self).get_initial()
        initial['user'] = self.request.user
        initial['schedule'] = self.schedule
        return initial

    def get_form_kwargs(self):
        # Force the submitted user to be request.user and the schedule to be
        # our chosen Schedule
        kwargs = super(AttendeeCreateUpdateView, self).get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs['data']['user'] = self.request.user.id
            kwargs['data']['schedule'] = self.schedule.id
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AttendeeCreateUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AttendeeCreateUpdateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AttendeeCreateUpdateView, self).get_context_data(**kwargs)
        context['schedule'] = self.schedule
        back_url = reverse('home')
        user_supplied_back_url = self.request.GET.get('back')
        if user_supplied_back_url and is_safe_url(user_supplied_back_url):
            back_url = user_supplied_back_url
        context['back_url'] = back_url
        return context


@login_required
def delete_photo(request):
    """
    A view specifically for deleting the photo attached to a profile so that
    we can do that via ajax and a nicer UI, rather than using Django's
    clearable file input (which is a bit clunky).
    """
    if request.method == 'POST' and request.is_ajax():
        # Delete the photo
        attendee = request.user.conference_attendee_profile
        sorl.thumbnail.delete(attendee.photo, delete_file=False)
        attendee.photo.delete()  # Saves the model automatically

        # Build a new form
        form_class = modelform_factory(Attendee, fields=['photo'])
        form = form_class(instance=attendee)
        form.fields['photo'].widget = forms.FileInput()

        # Render a response with the form and updated attendee
        html = render_to_string(
            'conference/_profile_photo.html',
            {'attendee': attendee, 'form': form}
        )
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest("This endpoint is only available to AJAX POST requests")
