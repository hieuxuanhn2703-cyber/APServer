import django.db.models.deletion
from django.db import migrations, models

def convert_nguoi_nhan_to_id(apps, schema_editor):
    MaterialIssue = apps.get_model('Inventory', 'MaterialIssue')
    AppUser = apps.get_model('Working', 'AppUser')
    default_user = AppUser.objects.filter(is_approved=True).first()
    if not default_user:
        default_user = AppUser.objects.first()
    
    default_id = str(default_user.id) if default_user else "1"

    for issue in MaterialIssue.objects.all():
        val = str(issue.nguoi_nhan).strip()
        matched = AppUser.objects.filter(name__icontains=val).first() or AppUser.objects.filter(account__icontains=val).first()
        if matched:
            issue.nguoi_nhan = str(matched.id)
        else:
            issue.nguoi_nhan = default_id
        issue.save()

class Migration(migrations.Migration):

    dependencies = [
        ('Working', '0022_alter_appuser_role'),
        ('Inventory', '0002_materialissue_receipt'),
    ]

    operations = [
        migrations.RunPython(convert_nguoi_nhan_to_id, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='materialissue',
            name='nguoi_nhan',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='received_material_issues',
                to='Working.appuser',
                verbose_name='Người nhận'
            ),
        ),
    ]
