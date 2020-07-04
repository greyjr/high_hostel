from django.db import models


class Client(models.Model):
    surname = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    patronymic = models.CharField(max_length=64)
    passport = models.CharField(max_length=128)
    another_document = models.CharField(max_length=128, null=True)
    phone = models.CharField(max_length=16)
    email = models.EmailField()
    comment = models.CharField(max_length=256, default='')

    def __str__(self):
        return self.surname + ' ' + self.name[0] + '. ' + self.patronymic[0] + '.'

    def all_client(self):
        return '{}, {}, {}'.format(self.__str__(), self.passport, self.phone)


class Room(models.Model):
    capacity = models.IntegerField()
    price = models.IntegerField()
    number = models.CharField(max_length=10)

    def __str__(self):
        return 'кімната ' + self.number


class Bed(models.Model):
    bed_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    number = models.IntegerField()

    def full_bed_name(self):
        return '{}.{}'.format(str(self.bed_room), str(self.number))

    def __str__(self):
        return 'кровать {} комната {}'.format(self.number, self.bed_room.number)


class Order(models.Model):
    order_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    order_bed = models.ForeignKey(Bed, on_delete=models.CASCADE, default=1)
    date_start = models.DateField()
    date_stop = models.DateField()

    def order_room(self):
        bed = Bed.objects.get(bed_room=self.order_bed)
        return Room.objects.get(number=bed.bed_room)

    def __str__(self):
        return '{}, {} {} - {}'.format(str(self.order_bed), str(self.order_client),
                                       str(self.date_start), str(self.date_stop))
