from django.db import models
import uuid


class Employee(models.Model):
    """Модель сотрудника
    Поля:
    - id: идентификатор
    - uuid: уникальный UUID
    - full_name: ФИО
    - photo: фотография сотрудника
    - created: дата создания
    - updated: дата обновления"""
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False, unique=True, verbose_name="UUID")
    full_name = models.CharField(max_length=512, verbose_name="ФИО")
    photo = models.ImageField(upload_to="employee", verbose_name="Фото")
    
    created = models.DateField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateField(auto_now=True, verbose_name="Обновлен")
    
    def __str__(self):
        return self.full_name
    

class EmployeeGroup(models.Model):
    """Группа сотрудников
    Поля:
    - id: идентификатор
    - uuid: уникальный UUID
    - title: наименование
    - employees: сотрудники в группе
    - created: дата создания
    - updated: дата обновления"""
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False, unique=True, verbose_name="UUID")
    title = models.CharField(max_length=256, verbose_name="Наименование")
    employees = models.ManyToManyField(to=Employee, blank=True, null=True)
    
    created = models.DateField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateField(auto_now=True, verbose_name="Обновлен")
    
    def __str__(self):
        return self.title


class Location(models.Model):
    """Расположения камер, замков, охранников, сотрудников
    Поля:
    - id: идентификатор
    - uuid: уникальный UUID
    - title: наименование
    - coordinates: координаты местоположения
    - created: дата создания
    - updated: дата обновления"""
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False, unique=True, verbose_name="UUID")
    title = models.CharField(max_length=4096, verbose_name="Название")
    coordinates = models.CharField(max_length=64, verbose_name="Координаты места")
    
    created = models.DateField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateField(auto_now=True, verbose_name="Обновлен")
    
    def __str__(self):
        return self.title
    
    
class Camera(models.Model):
    """Камера
    Поля:
    - id: уникальный идентификатор
    - uuid: уникальный UUID
    - camtype: тип камеры
    - ip_address: IP адрес камеры
    - location: местоположение камеры
    - created: дата создания
    - updated: дата обновления"""
    
    RECOGNIZE = 1
    CONTROL = 2
    
    camera_types = [
        (RECOGNIZE, "Распознающая"),
        (CONTROL, "Управляющая")
    ]
    
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False, unique=True, verbose_name="UUID")
    camtype = models.IntegerField(choices=camera_types, default=RECOGNIZE, verbose_name="Тип камеры")
    ip_address = models.CharField(max_length=32, verbose_name="IP адрес")
    location = models.ForeignKey(to=Location, db_index=True, on_delete=models.CASCADE, verbose_name="Расположение")
    
    created = models.DateField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateField(auto_now=True, verbose_name="Обновлен")
    
    def __str__(self):
        cam_type = self.get_camtype_display()
        cam_id = str(self.id)
        loc = self.location
        return f"{cam_type} камера #{cam_id}, {loc}, ({self.ip_address})"
    

class TourniquetLock(models.Model):
    """Турникеты
    Поля:
    - id: уникальный идентификатор
    - uuid: уникальный UUID
    - state: состояние (открыт/закрыт)
    - ip_address: IP адрес турникета/замка
    - location: местоположение турникета/замка
    - created: дата создания
    - updated: дата обновления"""
    
    TOURNIQUET = 1
    LOCK = 2
    
    tourniquet_types = [
        (TOURNIQUET, 'Турникет'),
        (LOCK, 'Замок')
    ]
    
    OPENED = 1
    CLOSED = 2
    
    tourniquet_states = [
        (OPENED, "Открыт"),
        (CLOSED, "Закрыт")
    ]
    
    lock_type = models.IntegerField(choices=tourniquet_types, db_index=True, default=TOURNIQUET, verbose_name="Тип")
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False, unique=True, verbose_name="UUID")
    state = models.IntegerField(choices=tourniquet_states, default=CLOSED, verbose_name="Состояние")
    ip_address = models.CharField(max_length=32, verbose_name="IP адрес")
    location = models.ForeignKey(to=Location, db_index=True, on_delete=models.CASCADE, verbose_name="Расположение")
    
    created = models.DateField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateField(auto_now=True, verbose_name="Обновлен")
    
    def __str__(self):
        lock_type = self.get_lock_type_display()
        lock_id = str(self.id)
        return f"{lock_type} #{lock_id} ({self.ip_address})"
    

class TourniquetTimeSheet(models.Model):
    """Табель доступа к турникету для сотрудника
    Поля:
    - id: уникальный идентификатор
    - uuid: уникальный UUID
    - employee: сотрудник
    - tourniquet: турникет/замок
    - start_time: начало времени доступа
    - end_time: окончание времени доступа
    - created: дата создания
    - updated: дата обновления"""
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False, unique=True, verbose_name="UUID")
    employee = models.ForeignKey(to=Employee, db_index=True, on_delete=models.CASCADE, verbose_name="Сотрудник")
    tourniquet = models.ForeignKey(to=TourniquetLock, db_index=True, on_delete=models.CASCADE, verbose_name="Турникет")
    start_time = models.TimeField(verbose_name="Время начала доступа")
    end_time = models.TimeField(verbose_name="Конец начала доступа")
    
    created = models.DateField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateField(auto_now=True, verbose_name="Обновлен")
    
    
class CameraToTourniquetLock(models.Model):
    """Связь камеры с турникетом/замком
    Поля:
    - id: уникальный идентификатор
    - uuid: уникальный UUID
    - tourniquet: турникет/замок
    - cameras: камеры, смотрящие на турникет/замок
    - created: дата создания
    - updated: дата обновления"""
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False, unique=True, verbose_name="UUID")
    tourniquet = models.ForeignKey(to=TourniquetLock, db_index=True, on_delete=models.CASCADE, verbose_name="Турникет")
    cameras = models.ManyToManyField(to=Camera)
    
    created = models.DateField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateField(auto_now=True, verbose_name="Обновлен")


class EmployeeGroupTimeSheet(models.Model):
    """Табель для группы сотрудников
    Поля:
    - id: уникальный идентификатор
    - uuid: уникальный UUID
    - employee_group: группа сотрудников
    - tourniquet: турникет/замок
    - start_time: время начала доступа
    - end_time: время окончания доступа"""
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False, unique=True, verbose_name="UUID")
    employee_group = models.ForeignKey(to=EmployeeGroup, db_index=True, on_delete=models.CASCADE, verbose_name="Группа сотрудников")
    tourniquet = models.ForeignKey(to=TourniquetLock, db_index=True, on_delete=models.CASCADE, verbose_name="Турникет")
    
    start_time = models.TimeField(verbose_name="Начало времени доступа")
    end_time = models.TimeField(verbose_name="Окончание времени доступа")
    
    created = models.DateField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateField(auto_now=True, verbose_name="Обновлен")