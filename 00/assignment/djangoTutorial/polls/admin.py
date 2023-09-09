from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]    # Choice 모델 클래스 같이 보기
    list_display = ["question_text", "pub_date", "was_published_recently"]    # Question 객체 리스트 컬럼 지정
    list_filter = ["pub_date"]  # 필터 사이드바 추가
    search_fields = ["question_text"]   # 검색 박스 추가


admin.site.register(Question, QuestionAdmin)   # admin 사이트에 Question 모델을 등록
