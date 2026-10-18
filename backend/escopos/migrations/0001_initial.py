import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Escopo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=500, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='LogAcesso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('permissao', models.CharField(blank=True, default='', max_length=500)),
                ('metodo', models.CharField(blank=True, default='', max_length=20)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='logs_acesso',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'ordering': ['-criado_em'],
            },
        ),
    ]
