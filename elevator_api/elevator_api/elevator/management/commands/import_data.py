import csv
from datetime import datetime
from django.core.management.base import BaseCommand

from elevator_api.elevator.models import Call, Elevator


class Command(BaseCommand):
    """A Django custom command to save elevator call data from a CSV file to a PostgreSQL database."""

    help = 'Comand to save the elevator data in PostgreSQL '

    def handle(self, *args, **options):
        """
            The main method that handles the command. Opens a CSV file, reads its contents, and saves the data
            to the PostgreSQL database using the Elevator and Call models.
        """

        csv_file = 'output.csv'
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            elevator_instance, _ = Elevator.objects.get_or_create(name='1', max_floors=10, current_floor=0)

            for row in reader:
                time = datetime.strptime(row['time'], '%Y-%m-%d %H:%M:%S.%f')
                origin = int(row['origin'])
                destination = int(row['destination'])
                current = int(row['current'])

                call = Call(elevator=elevator_instance, moment=time, source_floor=origin,
                            destination_floor=destination, rest_floor=current)
                call.save()
        self.stdout.write(self.style.SUCCESS('The data was saved successfully'))
