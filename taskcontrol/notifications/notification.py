from taskcontrol.models import *
from django.db.models import F ,Q, Case, When, Value, BooleanField
from datetime import datetime, timedelta
from django.shortcuts import render,redirect

#TODO Notification
def notification(request):
    # Filter EngagementDetail
    # #notification condition
    # ## status not equal 'Done'
    # ## Reviewer of approver
    # ## owner and near deadline or before deadline folow by notifation day

    # Check auth
    if request.user.is_authenticated:
        # Filter EngagementDetail
        engagement_result = EngagementDetail.objects.exclude(
                                Q(engagement__status='DONE',status='DONE')
                                    ).filter(
                                    (Q(engagement__create_by=request.user) | Q(engagement__reviewer= request.user) | Q(engagement__approver= request.user) | Q(engagement__administrator=request.user)) 
                                    &
                                    (
                                        Q(deadline__lte=datetime.today()) |
                                        Q(deadline__range=(datetime.now(),datetime.now() + timedelta(days=1)*(F('notification'))))
                                    )
                                ).annotate(
                                    is_over_deadline=Case(
                                        When(deadline__lte=datetime.now(),
                                            then=Value(True)
                                            ),
                                        default_value=Value(False),
                                        output_field=BooleanField()
                                    )
                                ).annotate(
                                    is_deadline=Case(
                                        When(deadline=datetime.now(),
                                            then=Value(True)
                                            ),
                                        default_value=Value(False),
                                        output_field=BooleanField()
                                    )
                                ).order_by('deadline')
        # Filter Task
        task_result = Task.objects.exclude(
                        Q(status='DONE')
                            ).filter(
                            Q(create_by=request.user) &
                        (
                            Q(due_date__lte=datetime.today()) |
                            Q(due_date__range=(datetime.now(),datetime.now()+timedelta(days=7)))
                        )
                        ).annotate(
                            is_deadline=Case(
                            When(due_date=datetime.now(),
                            then=Value(True)
                        ),
                            default_value=Value(False),
                            output_field=BooleanField()
                        )
                        ).order_by('due_date')
        # Filter Result
        # noti_result = engagement_result.union(task_result)
        return {
            'count': engagement_result.count() + task_result.count(),
            'notification_detail': engagement_result,
            'today_now': datetime.today(),
            'tasks_list': task_result
        }
    else :
        return {
            'count': 0,
            'notification_detail': [],
            'today_now': datetime.today(),
            'tasks_list': []
        }