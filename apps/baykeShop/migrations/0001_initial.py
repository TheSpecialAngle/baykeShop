# Generated by Django 4.1.5 on 2023-01-31 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaykeShopCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_del', models.BooleanField(default=False, editable=False, verbose_name='删除')),
                ('name', models.CharField(max_length=50, verbose_name='分类名称')),
                ('icon', models.CharField(blank=True, default='', max_length=50, verbose_name='分类icon')),
                ('img_map', models.ImageField(blank=True, max_length=200, null=True, upload_to='category/imgMap/%Y', verbose_name='分类图标')),
                ('desc', models.CharField(blank=True, default='', max_length=150, verbose_name='分类描述')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='baykeShop.baykeshopcategory')),
            ],
            options={
                'verbose_name': 'BaykeShopCategory',
                'verbose_name_plural': 'BaykeShopCategorys',
            },
        ),
        migrations.CreateModel(
            name='BaykeShopSpec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_del', models.BooleanField(default=False, editable=False, verbose_name='删除')),
                ('name', models.CharField(max_length=50, verbose_name='规格')),
            ],
            options={
                'verbose_name': 'BaykeShopSpec',
                'verbose_name_plural': 'BaykeShopSpecs',
            },
        ),
        migrations.CreateModel(
            name='BaykeShopSpecGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_del', models.BooleanField(default=False, editable=False, verbose_name='删除')),
                ('name', models.CharField(max_length=50, verbose_name='规格名称')),
            ],
            options={
                'verbose_name': 'BaykeShopSpecGroup',
                'verbose_name_plural': 'BaykeShopSpecGroups',
            },
        ),
        migrations.CreateModel(
            name='BaykeShopSPU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_del', models.BooleanField(default=False, editable=False, verbose_name='删除')),
                ('img', models.ImageField(max_length=200, upload_to='Carousel/%Y/%m', verbose_name='轮播图')),
                ('target_url', models.CharField(blank=True, default='', max_length=200, verbose_name='跳转链接')),
                ('title', models.CharField(max_length=150, verbose_name='商品名称')),
                ('keywords', models.CharField(blank=True, default='', max_length=150, verbose_name='商品关键字')),
                ('desc', models.CharField(blank=True, default='', max_length=200, verbose_name='商品描述')),
                ('unit', models.CharField(max_length=50, verbose_name='单位')),
                ('cover_pic', models.ImageField(max_length=200, upload_to='product/cover/spu/%Y/%m', verbose_name='封面图')),
                ('freight', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5, verbose_name='运费')),
                ('content', models.TextField(verbose_name='商品详情')),
                ('category', models.ManyToManyField(to='baykeShop.baykeshopcategory', verbose_name='商品分类')),
            ],
            options={
                'verbose_name': 'BaykeShopSPU',
                'verbose_name_plural': 'BaykeShopSPUs',
            },
        ),
        migrations.CreateModel(
            name='BaykeSPUCarousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_del', models.BooleanField(default=False, editable=False, verbose_name='删除')),
                ('img', models.ImageField(max_length=200, upload_to='Carousel/%Y/%m', verbose_name='轮播图')),
                ('target_url', models.CharField(blank=True, default='', max_length=200, verbose_name='跳转链接')),
                ('desc', models.CharField(blank=True, default='', max_length=150, verbose_name='描述')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baykeShop.baykeshopspu')),
            ],
            options={
                'verbose_name': 'BaykeSPUCarousel',
                'verbose_name_plural': 'BaykeSPUCarousels',
            },
        ),
        migrations.CreateModel(
            name='BaykeShopSpecOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_del', models.BooleanField(default=False, editable=False, verbose_name='删除')),
                ('name', models.CharField(max_length=50, verbose_name='规格值')),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baykeShop.baykeshopspec', verbose_name='规格')),
            ],
            options={
                'verbose_name': 'BaykeShopSpecOption',
                'verbose_name_plural': 'BaykeShopSpecOptions',
            },
        ),
        migrations.AddField(
            model_name='baykeshopspec',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baykeShop.baykeshopspecgroup', verbose_name='规格组'),
        ),
        migrations.CreateModel(
            name='BaykeShopSKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_del', models.BooleanField(default=False, editable=False, verbose_name='删除')),
                ('cover_pic', models.ImageField(height_field='800', max_length=200, upload_to='cover/sku/%Y/%m', verbose_name='封面图', width_field='800')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='售价')),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='成本价')),
                ('org_price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='原价')),
                ('stock', models.IntegerField(default=0, verbose_name='库存')),
                ('numname', models.CharField(blank=True, default='', max_length=50, verbose_name='商品编号')),
                ('weight', models.FloatField(blank=True, default=0, verbose_name='重量(KG)')),
                ('vol', models.FloatField(blank=True, default=0, verbose_name='体积(m³)')),
                ('options', models.ManyToManyField(blank=True, to='baykeShop.baykeshopspecoption', verbose_name='商品规格')),
                ('spu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baykeShop.baykeshopspu', verbose_name='商品')),
            ],
            options={
                'verbose_name': 'BaykeShopSKU',
                'verbose_name_plural': 'BaykeShopSKUs',
            },
        ),
    ]
