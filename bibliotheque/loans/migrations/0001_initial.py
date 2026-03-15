from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_date', models.DateField(default=django.utils.timezone.now)),
                ('due_date', models.DateField()),
                ('return_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('en_cours', 'En cours'), ('retourne', 'Retourné')], default='en_cours', max_length=20)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='loans', to='books.book')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-loan_date']},
        ),
    ]
