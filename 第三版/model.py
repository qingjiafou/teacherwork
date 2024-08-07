# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from database import db
from sqlalchemy import event, func
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash


class TeacherInformation(db.Model):
    __tablename__ = 'teacher_information'

    teacher_id = db.Column(db.String(255), primary_key=True, info={'description': '教工号'})
    teacher_name = db.Column(db.String(255), info={'description': '教师姓名'})
    password_hash = db.Column(db.String(255), info={'description': 'hash密码'})

    @property
    def password(self):
        raise ArithmeticError("password是不可读字段")

    # 设置密码，加密，比如,xxx.password=xxxx
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)



class CompetitionAward(db.Model):
    __tablename__ = 'competition_awards'

    id = db.Column(db.Integer, primary_key=True, info={'description': '序号'})
    event_name = db.Column(db.String(24), info={'description': '赛事名称'})
    work_name = db.Column(db.String(24), info={'description': '作品名称'})
    award_category = db.Column(db.String(24), info={'description': '获奖类别'})
    award_level = db.Column(db.String(24), info={'description': '获奖等级'})
    teacher_name = db.Column(db.String(24), info={'description': '指导教师'})
    teacher_id = db.Column(db.String(24), db.ForeignKey('teacher_information.teacher_id'), index=True,
                           info={'description': '指导教师工号'})
    total_workload = db.Column(db.Float(precision=6, asdecimal=True), info={'description': '总工作量'})
    award_year = db.Column(db.String(24), info={'description': '获奖年份'})

    teacher = db.relationship('TeacherInformation', backref='competition_awards')

    @classmethod
    def CompetitionAward_list(cls):
        return cls.query.all()

    @classmethod
    def add_competition_award(cls, event_name, work_name, award_category, award_level, teacher_name, teacher_id,
                              total_workload, award_year):
        new_award = CompetitionAward(
            event_name=event_name,
            work_name=work_name,
            award_category=award_category,
            award_level=award_level,
            teacher_name=teacher_name,
            teacher_id=teacher_id,
            total_workload=total_workload,
            award_year=award_year
        )
        db.session.add(new_award)
        db.session.commit()


class DepartmentInternship(db.Model):
    __tablename__ = 'department_internship'

    student_name = db.Column(db.String(24), info={'description': '学生姓名'})
    student_id = db.Column(db.String(24), primary_key=True, info={'description': '学生学号'})
    major = db.Column(db.String(24), info={'description': '专业'})
    grade = db.Column(db.String(24), info={'description': '年级'})
    teacher_name = db.Column(db.String(24), info={'description': '学部内实习指导教师'})
    teacher_id = db.Column(db.String(24), db.ForeignKey('teacher_information.teacher_id'),
                           index=True, info={'description': '学部内实习指导教师工号'})
    week = db.Column(db.String(24), info={'description': '实习周数'})
    teacher = db.relationship('TeacherInformation',
                              primaryjoin='DepartmentInternship.teacher_id == TeacherInformation.teacher_id',
                              backref='department_internships')

    def DepartmentInternship_list(self):
        return [self.student_name, self.student_id, self.major, self.grade, self.teacher_name, self.teacher_id]

    def add_internship_record(self, student_name, student_id, major, grade, teacher_name, teacher_id):
        new_internship = DepartmentInternship(
            student_name=student_name,
            student_id=student_id,
            major=major,
            grade=grade,
            teacher_name=teacher_name,
            teacher_id=teacher_id
        )
        db.session.add(new_internship)
        db.session.commit()


class EducationalResearchProject(db.Model):
    __tablename__ = 'educational_research_project'

    id = db.Column(db.Integer, primary_key=True, info={'description': '序号，主键'})
    project_name = db.Column(db.String(24), info={'description': '项目名称'})
    project_leader = db.Column(db.String(24), info={'description': '项目负责人'})
    project_members = db.Column(db.String(24), info={'description': '项目成员'})
    project_level = db.Column(db.String(24), info={'description': '级别'})
    start_date = db.Column(db.Date, info={'description': '立项时间'})
    end_date = db.Column(db.Date, info={'description': '结项时间'})
    acceptance_result = db.Column(db.String(24), info={'description': '验收结论'})
    teacher_name = db.Column(db.String(24), info={'description': '教师姓名'})
    teacher_id = db.Column(db.String(24), db.ForeignKey('teacher_information.teacher_id'),
                           index=True, info={'description': '工号'})
    research_project_workload = db.Column(db.Float(precision=6, asdecimal=True),
                                          info={'description': '教研项目工作量'})

    teacher = db.relationship('TeacherInformation',
                              primaryjoin='EducationalResearchProject.teacher_id == TeacherInformation.teacher_id',
                              backref='educational_research_projects')

    def EducationalResearchProject_list(self):
        return [
            self.id,
            self.project_name, self.project_leader, self.project_members, self.project_level, self.start_date,
            self.end_date, self.acceptance_result, self.teacher_name, self.teacher_id, self.research_project_workload
        ]

    def add_research_project(self, project_name, project_leader, project_members, project_level, start_date, end_date,
                             acceptance_result, teacher_name, teacher_id, research_project_workload):
        new_project = EducationalResearchProject(
            project_name=project_name,
            project_leader=project_leader,
            project_members=project_members,
            project_level=project_level,
            start_date=start_date,
            end_date=end_date,
            acceptance_result=acceptance_result,
            teacher_name=teacher_name,
            teacher_id=teacher_id,
            research_project_workload=research_project_workload
        )
        db.session.add(new_project)
        db.session.commit()


class FirstClassCourse(db.Model):
    __tablename__ = 'first_class_courses'

    id = db.Column(db.Integer, primary_key=True, info={'description': '序号'})
    course_type = db.Column(db.String(24), info={'description': '课程性质'})
    content = db.Column(db.String(24), info={'description': '内容'})
    leader = db.Column(db.String(24), info={'description': '负责人'})
    remark = db.Column(db.String(24), info={'description': '备注，工作量分配'})
    teacher_name = db.Column(db.String(24), info={'description': '教师姓名，一位老师一个记录'})
    teacher_id = db.Column(db.String(24), db.ForeignKey('teacher_information.teacher_id'),
                           index=True, info={'description': '工号，外键'})
    first_class_course_workload = db.Column(db.Float(precision=6, asdecimal=True),
                                            info={'description': '一流课程工作量'})

    teacher = db.relationship('TeacherInformation',
                              primaryjoin='FirstClassCourse.teacher_id == TeacherInformation.teacher_id',
                              backref='first_class_courses')

    def FirstClassCourse_list(self):
        return [
            self.id,
            self.course_type,
            self.content,
            self.leader,
            self.remark,
            self.teacher_name,
            self.teacher_id,
            self.first_class_course_workload,
        ]

    def add_first_class_course(self, course_type, content, leader, remark, teacher_name, teacher_id,
                               first_class_course_workload):
        new_course = FirstClassCourse(
            course_type=course_type,
            content=content,
            leader=leader,
            remark=remark,
            teacher_name=teacher_name,
            teacher_id=teacher_id,
            first_class_course_workload=first_class_course_workload
        )
        db.session.add(new_course)
        db.session.commit()


class PublicService(db.Model):
    __tablename__ = 'public_services'

    id = db.Column(db.Integer, primary_key=True, info={'description': '序号，主键，自增，无意义'})
    serve_date = db.Column(db.String(24), info={'description': '日期'})
    content = db.Column(db.String(24), info={'description': '内容'})
    teacher_name = db.Column(db.String(24), info={'description': '姓名'})
    work_duration = db.Column(db.Float(precision=6, asdecimal=True), info={'description': '工作时长'})
    class_hours = db.Column(db.Float(precision=6, asdecimal=True), info={'description': '课时'})
    teacher_id = db.Column(db.String(24), db.ForeignKey('teacher_information.teacher_id'),
                           index=True, info={'description': '教师工号，外键'})
    workload = db.Column(db.Float, info={'description': '工作量'})
    teacher = db.relationship('TeacherInformation',
                              primaryjoin='PublicService.teacher_id == TeacherInformation.teacher_id',
                              backref='public_services')

    def PublicService_list(self):
        return [
            self.id,
            self.serve_date,
            self.content,
            self.teacher_name,
            self.work_duration,
            self.class_hours,
            self.teacher_id
        ]

    def add_public_service_record(self, serve_date, content, teacher_name, work_duration, class_hours, teacher_id):
        new_record = PublicService(
            serve_date=serve_date,
            content=content,
            teacher_name=teacher_name,
            work_duration=work_duration,
            class_hours=class_hours,
            teacher_id=teacher_id
        )
        db.session.add(new_record)
        db.session.commit()


class StudentResearch(db.Model):
    __tablename__ = 'student_research'

    id = db.Column(db.Integer, primary_key=True, info={'description': '序号'})
    project_name = db.Column(db.String(24), info={'description': '项目名称'})
    project_level = db.Column(db.String(24), info={'description': '级别'})
    leader = db.Column(db.String(24), info={'description': '负责人'})
    student_id = db.Column(db.String(24), info={'description': '学号'})
    total_members = db.Column(db.Integer, info={'description': '项目组总人数'})
    teacher_name = db.Column(db.String(24), info={'description': '指导老师'})
    teacher_id = db.Column(db.ForeignKey('teacher_information.teacher_id'), index=True,
                           info={'description': '指导老师工号'})
    acceptance_result = db.Column(db.String(24), info={'description': '验收结果'})
    workload = db.Column(db.Float(precision=6, asdecimal=True), info={'description': '工作量'})

    teacher = db.relationship('TeacherInformation',
                              primaryjoin='StudentResearch.teacher_id == TeacherInformation.teacher_id',
                              backref='student_researches')

    def StudentResearch_list(self):
        return [
            self.id, self.project_name, self.project_level,
            self.leader, self.student_id, self.total_members,
            self.teacher_name, self.teacher_id, self.acceptance_result,
            self.workload
        ]

    def add_student_research_record(self, project_name, project_level, leader, student_id, total_members, teacher_name,
                                    teacher_id, acceptance_result, workload):
        new_record = StudentResearch(
            project_name=project_name,
            project_level=project_level,
            leader=leader,
            student_id=student_id,
            total_members=total_members,
            teacher_name=teacher_name,
            teacher_id=teacher_id,
            acceptance_result=acceptance_result,
            workload=workload
        )
        db.session.add(new_record)
        db.session.commit()


class TeachingAchievementAward(db.Model):
    __tablename__ = 'teaching_achievement_awards'

    id = db.Column(db.Integer, primary_key=True, info={'description': '序号，主键，自增，无意义'})
    student_session = db.Column(db.String(24), info={'description': '届'})
    student_date = db.Column(db.String(24), info={'description': '时间'})
    recommended_achievement_name = db.Column(db.String(24), info={'description': '推荐成果名称'})
    main_completion_person_name = db.Column(db.String(24), info={'description': '成果主要完成人名称'})
    award_category = db.Column(db.String(24), info={'description': '获奖类别'})
    award_level = db.Column(db.String(24), info={'description': '获奖等级'})
    remark = db.Column(db.String(24), info={'description': '备注'})
    teacher_name = db.Column(db.String(24), info={'description': '教师'})
    teacher_id = db.Column(db.ForeignKey('teacher_information.teacher_id'), index=True,
                           info={'description': '工号，外键'})
    teaching_achievement_workload = db.Column(db.Float(precision=6, asdecimal=True),
                                              info={'description': '教学成果工作量'})

    teacher = db.relationship('TeacherInformation',
                              primaryjoin='TeachingAchievementAward.teacher_id == TeacherInformation.teacher_id',
                              backref='teaching_achievement_awards')

    def TeachingAchievementAward_list(self):
        return [
            self.id, self.student_session, self.student_date,
            self.recommended_achievement_name, self.main_completion_person_name,
            self.award_category, self.award_level, self.remark,
            self.teacher_name, self.teacher_id, self.teaching_achievement_workload
        ]

    def add_teaching_achievement_record(self, student_session, student_date, recommended_achievement_name,
                                        main_completion_person_name, award_category, award_level, remark, teacher_name,
                                        teacher_id, teaching_achievement_workload):
        new_record = TeachingAchievementAward(
            student_session=student_session,
            student_date=student_date,
            recommended_achievement_name=recommended_achievement_name,
            main_completion_person_name=main_completion_person_name,
            award_category=award_category,
            award_level=award_level,
            remark=remark,
            teacher_name=teacher_name,
            teacher_id=teacher_id,
            teaching_achievement_workload=teaching_achievement_workload
        )
        db.session.add(new_record)
        db.session.commit()


class UndergraduateMentorshipSystem(db.Model):
    __tablename__ = 'undergraduate_mentorship_system'

    teacher_name = db.Column(db.String(24), info={'description': '导师姓名'})
    teacher_id = db.Column(db.ForeignKey('teacher_information.teacher_id'), index=True,
                           info={'description': '教工号'})
    student_name = db.Column(db.String(24), info={'description': '学生姓名'})
    grade = db.Column(db.String(24), info={'description': '年级'})
    student_id = db.Column(db.String(24), primary_key=True, info={'description': '学号'})
    teacher_workload = db.Column(db.Float(precision=6, asdecimal=True), info={'description': '教师工作量'})

    teacher = db.relationship('TeacherInformation',
                              primaryjoin='UndergraduateMentorshipSystem.teacher_id == TeacherInformation.teacher_id',
                              backref='undergraduate_mentorship_systems')

    def UndergraduateMentorshipSystem_list(self):
        return [
            self.teacher_name, self.teacher_id, self.student_name,
            self.grade, self.student_id, self.teacher_workload
        ]

    def add_mentorship_record(self, teacher_name, teacher_id, student_name, grade, student_id, teacher_workload):
        new_record = UndergraduateMentorshipSystem(
            teacher_name=teacher_name,
            teacher_id=teacher_id,
            student_name=student_name,
            grade=grade,
            student_id=student_id,
            teacher_workload=teacher_workload
        )
        db.session.add(new_record)
        db.session.commit()


class UndergraduateThesi(db.Model):
    __tablename__ = 'undergraduate_thesis'

    student_name = db.Column(db.String(24), info={'description': '学生姓名'})
    student_id = db.Column(db.String(24), primary_key=True, info={'description': '学生学号'})
    college = db.Column(db.String(24), info={'description': '学院'})
    major = db.Column(db.String(24), info={'description': '专业'})
    major_id = db.Column(db.String(24), info={'description': '专业号'})
    grade = db.Column(db.String(24), info={'description': '年级'})
    thesis_topic = db.Column(db.String(24), info={'description': '毕业论文题目'})
    thesis_grade = db.Column(db.String(24), info={'description': '毕业论文成绩'})
    teacher_name = db.Column(db.String(24), info={'description': '毕业论文指导老师'})
    teacher_id = db.Column(db.ForeignKey('teacher_information.teacher_id'), index=True,
                           info={'description': '毕业论文指导老师工号'})

    teacher = db.relationship('TeacherInformation',
                              primaryjoin='UndergraduateThesi.teacher_id == TeacherInformation.teacher_id',
                              backref='undergraduate_thesis')

    def UndergraduateThesi_list(self):
        return [
            self.student_name, self.student_id, self.college, self.major, self.major_id,
            self.grade, self.thesis_topic, self.thesis_grade, self.teacher_name, self.teacher_id
        ]

    def add_thesis_record(self, student_name, student_id, college, major, major_id, grade, thesis_topic, thesis_grade,
                          teacher_name, teacher_id):
        new_record = UndergraduateThesi(
            student_name=student_name,
            student_id=student_id,
            college=college,
            major=major,
            major_id=major_id,
            grade=grade,
            thesis_topic=thesis_topic,
            thesis_grade=thesis_grade,
            teacher_name=teacher_name,
            teacher_id=teacher_id
        )
        db.session.add(new_record)
        db.session.commit()


class UndergraduateWorkloadCourseRanking(db.Model):
    __tablename__ = 'undergraduate_workload_course_ranking'

    academic_year = db.Column(db.String(10), info={'description': '学年'})
    semester = db.Column(db.String(10), info={'description': '学期'})
    calendar_year = db.Column(db.Integer, info={'description': '自然年'})
    half_year = db.Column(db.String(20), info={'description': '上下半年'})
    course_code = db.Column(db.String(24), primary_key=True, nullable=False, info={'description': '课程号'})
    teaching_class = db.Column(db.String(24), primary_key=True, nullable=False, info={'description': '教学班'})
    course_name = db.Column(db.String(100), info={'description': '课程名称'})  # 调整长度
    teacher_id = db.Column(db.String(30), db.ForeignKey('teacher_information.teacher_id'),
                           index=True, info={'description': '教工号'})  # 调整长度
    teacher_name = db.Column(db.String(50), info={'description': '教师名称'})  # 调整长度
    seminar_hours = db.Column(db.Float, info={'description': '研讨学时'})  # 调整类型为Float
    lecture_hours = db.Column(db.Float, info={'description': '授课学时'})  # 调整类型为Float
    lab_hours = db.Column(db.Float, info={'description': '实验学时'})  # 调整类型为Float
    enrolled_students = db.Column(db.Integer, info={'description': '选课人数'})
    student_weight_coefficient_b = db.Column(db.Float, info={'description': '学生数量权重系数B'})  # 调整类型为Float
    course_type_coefficient_a = db.Column(db.Float, info={'description': '课程类型系数A'})  # 调整类型为Float
    total_lecture_hours_p1 = db.Column(db.Float, info={'description': '理论课总学时P1'})  # 调整类型为Float
    lab_group_count = db.Column(db.Integer, info={'description': '实验分组数'})
    lab_coefficient = db.Column(db.Float, info={'description': '实验课系数'})  # 调整类型为Float
    total_lab_hours_p2 = db.Column(db.Float, info={'description': '实验课总学时P2'})  # 调整类型为Float
    course_split_ratio_for_engineering_center = db.Column(db.Float, info={
        'description': '课程拆分占比（工程中心用）'})  # 调整类型为Float
    total_course_hours = db.Column(db.Float, info={'description': '课程总学时'})  # 调整类型为Float

    # 修改外键关系设置
    teacher = db.relationship('TeacherInformation',
                              primaryjoin='UndergraduateWorkloadCourseRanking.teacher_id == TeacherInformation.teacher_id',
                              backref='undergraduate_workload_course_rankings')

    def UndergraduateWorkloadCourseRanking_list(self):
        return [
            self.academic_year, self.semester, self.calendar_year, self.half_year, self.course_code,
            self.teaching_class, self.course_name, self.teacher_id, self.teacher_name, self.seminar_hours,
            self.lecture_hours, self.lab_hours, self.enrolled_students, self.student_weight_coefficient_b,
            self.course_type_coefficient_a, self.total_lecture_hours_p1, self.lab_group_count, self.lab_coefficient,
            self.total_lab_hours_p2, self.course_split_ratio_for_engineering_center,
            self.total_course_hours
        ]

    def add_course_ranking(self, academic_year, semester, calendar_year, half_year, course_code, teaching_class,
                           course_name, teacher_id, teacher_name, seminar_hours, lecture_hours, lab_hours,
                           enrolled_students, student_weight_coefficient_b, course_type_coefficient_a,
                           total_lecture_hours_p1, lab_group_count, lab_coefficient, total_lab_hours_p2,
                           course_split_ratio_for_engineering_center,
                           total_course_hours):
        new_course_ranking = UndergraduateWorkloadCourseRanking(
            academic_year=academic_year,
            semester=semester,
            calendar_year=calendar_year,
            half_year=half_year,
            course_code=course_code,
            teaching_class=teaching_class,
            course_name=course_name,
            teacher_id=teacher_id,
            teacher_name=teacher_name,
            seminar_hours=seminar_hours,
            lecture_hours=lecture_hours,
            lab_hours=lab_hours,
            enrolled_students=enrolled_students,
            student_weight_coefficient_b=student_weight_coefficient_b,
            course_type_coefficient_a=course_type_coefficient_a,
            total_lecture_hours_p1=total_lecture_hours_p1,
            lab_group_count=lab_group_count,
            lab_coefficient=lab_coefficient,
            total_lab_hours_p2=total_lab_hours_p2,
            course_split_ratio_for_engineering_center=course_split_ratio_for_engineering_center,
            total_course_hours=total_course_hours
        )
        db.session.add(new_course_ranking)
        db.session.commit()


class UndergraduateWorkloadTeacherRanking(db.Model):
    __tablename__ = 'undergraduate_workload_teacher_ranking'

    id = db.Column(db.Integer, primary_key=True, info={'description': '序号，主键，自增，无意义'})
    teacher_id = db.Column(db.String(30), db.ForeignKey('teacher_information.teacher_id'),
                           info={'description': '教工号'})
    teacher_name = db.Column(db.String(50), info={'description': '教师名称'})  # 调整长度
    undergraduate_course_total_hours = db.Column(db.Float, info={'description': '本科课程总学时'})
    graduation_thesis_student_count = db.Column(db.Integer, info={'description': '毕业论文学生人数'})
    graduation_thesis_p = db.Column(db.Float, info={'description': '毕业论文P'})
    teaching_internship_student_count = db.Column(db.Integer, info={'description': '指导教学实习人数'})
    teaching_internship_weeks = db.Column(db.Integer, info={'description': '指导教学实习周数'})
    teaching_internship_p = db.Column(db.Float, info={'description': '指导教学实习P'})
    responsible_internship_construction_management_p = db.Column(db.Float,
                                                                 info={'description': '负责实习点建设与管理P'})
    guiding_undergraduate_competition_p = db.Column(db.Float, info={'description': '指导本科生竞赛P'})
    guiding_undergraduate_research_p = db.Column(db.Float, info={'description': '指导本科生科研P'})
    undergraduate_tutor_system = db.Column(db.Float, info={'description': '本科生导师制'})
    teaching_research_and_reform_p = db.Column(db.Float, info={'description': '教研教改P'})
    first_class_course = db.Column(db.Float, info={'description': '一流课程'})
    teaching_achievement_award = db.Column(db.Float, info={'description': '教学成果奖'})
    public_service = db.Column(db.Float, info={'description': '公共服务'})
    # 修改外键关系设置
    teacher = db.relationship('TeacherInformation',
                              primaryjoin='UndergraduateWorkloadTeacherRanking.teacher_id == TeacherInformation.teacher_id',
                              backref='undergraduate_workload_teacher_ranking')

    def UndergraduateWorkloadTeacherRanking_list(self):
        return [
            self.teacher_id, self.teacher_name,
            self.undergraduate_course_total_hours,
            self.graduation_thesis_student_count, self.graduation_thesis_p,
            self.teaching_internship_student_count, self.teaching_internship_weeks,
            self.teaching_internship_p, self.responsible_internship_construction_management_p,
            self.guiding_undergraduate_competition_p, self.guiding_undergraduate_research_p,
            self.undergraduate_tutor_system, self.teaching_research_and_reform_p,
            self.first_class_course, self.teaching_achievement_award, self.public_service
        ]

    def add_teacher_ranking(self, teacher_id, teacher_name, undergraduate_course_total_hours,
                            graduation_thesis_student_count, graduation_thesis_p, teaching_internship_student_count,
                            teaching_internship_weeks, teaching_internship_p,
                            responsible_internship_construction_management_p, guiding_undergraduate_competition_p,
                            guiding_undergraduate_research_p, undergraduate_tutor_system,
                            teaching_research_and_reform_p, first_class_course, teaching_achievement_award,
                            public_service):
        new_teacher_ranking = UndergraduateWorkloadTeacherRanking(
            teacher_id=teacher_id,
            teacher_name=teacher_name,
            undergraduate_course_total_hours=undergraduate_course_total_hours,
            graduation_thesis_student_count=graduation_thesis_student_count,
            graduation_thesis_p=graduation_thesis_p,
            teaching_internship_student_count=teaching_internship_student_count,
            teaching_internship_weeks=teaching_internship_weeks,
            teaching_internship_p=teaching_internship_p,
            responsible_internship_construction_management_p=responsible_internship_construction_management_p,
            guiding_undergraduate_competition_p=guiding_undergraduate_competition_p,
            guiding_undergraduate_research_p=guiding_undergraduate_research_p,
            undergraduate_tutor_system=undergraduate_tutor_system,
            teaching_research_and_reform_p=teaching_research_and_reform_p,
            first_class_course=first_class_course,
            teaching_achievement_award=teaching_achievement_award,
            public_service=public_service
        )
        db.session.add(new_teacher_ranking)
        db.session.commit()


class workload_parameter(db.Model):
    __tablename__ = 'workload_parameter'

    id = db.Column(db.Integer, primary_key=True, info={'description': '序号'})
    graduation_thesis_p_count = db.Column(db.Float, info={'description': '毕业论文参数'})
    intership_count = db.Column(db.Float, info={'description': '指导实习参数'})
    intership_js = db.Column(db.Float, info={'description': '实习点建设'})


# 触发器


def update_undergraduate_course_total_hours(mapper, connection, target):
    session = Session(bind=connection)
    course = session.query(UndergraduateWorkloadTeacherRanking).filter_by(teacher_id=target.teacher_id).one()
    course.undergraduate_course_total_hours = session.query(
        func.sum(mapper.c.total_course_hours)). \
        filter(mapper.c.teacher_id == target.teacher_id). \
        scalar()
    session.commit()


def update_graduation_thesis_info(mapper, connection, target):
    session = Session(bind=connection)
    teacher_id = target.teacher_id

    # 更新毕业论文学生数量
    graduation_thesis_student_count = (
        session.query(func.count(mapper.c.student_id))
        .filter(mapper.c.teacher_id == teacher_id)
        .scalar()
    )

    # 查询毕业论文工作量参数
    graduation_thesis_p_count = session.query(workload_parameter.graduation_thesis_p_count).scalar()

    # 计算毕业论文工作量
    graduation_thesis_p = graduation_thesis_p_count * graduation_thesis_student_count

    # 查询该教师的记录
    teacher = session.query(UndergraduateWorkloadTeacherRanking).filter_by(teacher_id=teacher_id).one()

    # 更新毕业论文学生数量字段
    teacher.graduation_thesis_student_count = graduation_thesis_student_count

    # 更新毕业论文工作量字段
    teacher.graduation_thesis_p = graduation_thesis_p

    session.commit()


def update_teaching_internship_student_info(mapper, connection, target):
    session = Session(bind=connection)
    teacher_id = target.teacher_id
    # 更新指导教学实习的人数
    internship_student_count = session.query(
        func.count(mapper.c.student_id).filter(mapper.c.teacher_id == teacher_id).scalar())
    # 更新指导教学实习的周数
    internship_week_count = session.query(
        func.sum(mapper.c.week).filter(mapper.c.teacher_id == teacher_id).scalar())
    # 查询教学实习指导的参数
    internship_count = session.query(workload_parameter.internship_count).scalar()
    # 查询教学实习点的建设与管理P，这个直接查表得到
    internship_js = session.query(workload_parameter.internship_js).scalar()
    # 更新指导教学实习P
    teaching_internship_student_count = internship_student_count * internship_week_count * internship_count
    # 查询该教师的记录并更新
    teacher = session.query(UndergraduateWorkloadTeacherRanking).filter_by(teacher_id=teacher_id).one()
    teacher.teaching_internship_student_count = internship_student_count
    teacher.teaching_internship_weeks = internship_week_count
    teacher.teaching_internship_p = teaching_internship_student_count
    teacher.responsible_internship_construction_management_p = internship_js
    session.commit()


def update_guiding_undergraduate_competition_p(mapper, connection, target):
    session = Session(bind=connection)
    course = session.query(UndergraduateWorkloadTeacherRanking).filter_by(teacher_id=target.teacher_id).one()
    course.undergraduate_course_total_hours = session.query(
        func.sum(mapper.c.total_workload)). \
        filter(mapper.c.teacher_id == target.teacher_id). \
        scalar()
    session.commit()


def update_guiding_undergraduate_research_p(mapper, connection, target):
    session = Session(bind=connection)
    course = session.query(UndergraduateWorkloadTeacherRanking).filter_by(teacher_id=target.teacher_id).one()
    course.undergraduate_course_total_hours = session.query(
        func.sum(mapper.c.workload)). \
        filter(mapper.c.teacher_id == target.teacher_id). \
        scalar()
    session.commit()


def update_undergraduate_tutor_system(mapper, connection, target):
    session = Session(bind=connection)
    course = session.query(UndergraduateWorkloadTeacherRanking).filter_by(teacher_id=target.teacher_id).one()
    course.undergraduate_course_total_hours = session.query(
        func.sum(mapper.c.teacher_workload)). \
        filter(mapper.c.teacher_id == target.teacher_id). \
        scalar()
    session.commit()


def update_teaching_research_and_reform_p(mapper, connection, target):
    session = Session(bind=connection)
    course = session.query(UndergraduateWorkloadTeacherRanking).filter_by(teacher_id=target.teacher_id).one()
    course.undergraduate_course_total_hours = session.query(
        func.sum(mapper.c.research_project_workload)). \
        filter(mapper.c.teacher_id == target.teacher_id). \
        scalar()
    session.commit()


def update_first_class_course(mapper, connection, target):
    session = Session(bind=connection)
    course = session.query(UndergraduateWorkloadTeacherRanking).filter_by(teacher_id=target.teacher_id).one()
    course.undergraduate_course_total_hours = session.query(
        func.sum(mapper.c.first_class_course_workload)). \
        filter(mapper.c.teacher_id == target.teacher_id). \
        scalar()
    session.commit()


def update_teaching_achievement_award(mapper, connection, target):
    session = Session(bind=connection)
    course = session.query(UndergraduateWorkloadTeacherRanking).filter_by(teacher_id=target.teacher_id).one()
    course.undergraduate_course_total_hours = session.query(
        func.sum(mapper.c.teaching_achievement_workload)). \
        filter(mapper.c.teacher_id == target.teacher_id). \
        scalar()
    session.commit()


def update_public_service(mapper, connection, target):
    session = Session(bind=connection)
    course = session.query(UndergraduateWorkloadTeacherRanking).filter_by(teacher_id=target.teacher_id).one()
    course.undergraduate_course_total_hours = session.query(
        func.sum(mapper.c.workload)). \
        filter(mapper.c.teacher_id == target.teacher_id). \
        scalar()
    session.commit()


# 触发器监听
db.event.listen(UndergraduateWorkloadCourseRanking, 'after_insert', update_undergraduate_course_total_hours)
db.event.listen(UndergraduateWorkloadCourseRanking, 'after_update', update_undergraduate_course_total_hours)
# 有几个触发器需要传递几个可变参数来计算工作量，将参数全部放在一张表里面了
db.event.listen(UndergraduateThesi, 'after_insert', update_graduation_thesis_info)
db.event.listen(UndergraduateThesi, 'after_update', update_graduation_thesis_info)
db.event.listen(DepartmentInternship, 'after_insert', update_teaching_internship_student_info)
db.event.listen(DepartmentInternship, 'after_update', update_teaching_internship_student_info)
db.event.listen(CompetitionAward, 'after_insert', update_guiding_undergraduate_competition_p)
db.event.listen(CompetitionAward, 'after_update', update_guiding_undergraduate_competition_p)
db.event.listen(StudentResearch, 'after_insert', update_guiding_undergraduate_research_p)
db.event.listen(StudentResearch, 'after_update', update_guiding_undergraduate_research_p)
db.event.listen(UndergraduateMentorshipSystem, 'after_insert', update_undergraduate_tutor_system)
db.event.listen(UndergraduateMentorshipSystem, 'after_update', update_undergraduate_tutor_system)
db.event.listen(EducationalResearchProject, 'after_insert', update_teaching_research_and_reform_p)
db.event.listen(EducationalResearchProject, 'after_update', update_teaching_research_and_reform_p)
db.event.listen(FirstClassCourse, 'after_insert', update_first_class_course)
db.event.listen(FirstClassCourse, 'after_update', update_first_class_course)
db.event.listen(TeachingAchievementAward, 'after_insert', update_teaching_achievement_award)
db.event.listen(TeachingAchievementAward, 'after_update', update_teaching_achievement_award)
db.event.listen(PublicService, 'after_insert', update_public_service)
db.event.listen(PublicService, 'after_update', update_public_service)
