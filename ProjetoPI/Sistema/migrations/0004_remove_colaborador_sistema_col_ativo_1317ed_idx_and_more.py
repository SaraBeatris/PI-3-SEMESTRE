# Generated by Django 5.2.1 on 2025-06-04 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0003_hotel_delete_refeicao'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='colaborador',
            name='Sistema_col_ativo_1317ed_idx',
        ),
        migrations.RemoveField(
            model_name='colaborador',
            name='ativo',
        ),
        migrations.RemoveField(
            model_name='colaborador',
            name='cidade',
        ),
        migrations.RemoveField(
            model_name='colaborador',
            name='desconto',
        ),
        migrations.RemoveField(
            model_name='colaborador',
            name='foto',
        ),
        migrations.RemoveField(
            model_name='colaborador',
            name='observacoes',
        ),
        migrations.AddField(
            model_name='colaborador',
            name='endereco',
            field=models.CharField(default='SEM ENDEREÇO', max_length=50, verbose_name='Endereço'),
            preserve_default=False,
        ),
    ]
