# -*- coding: utf-8 -*-
# @Time    : 2022/6/6 14:22
# @Author  : 臧成龙
# @FileName: usual.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404

from system.models import Users
from utils.fu_auth import data_permission
from utils.fu_ninga import FuFilters
from utils.usual import get_user_info_from_token, get_dept


def create(request, data, model):
    if not isinstance(data, dict):
        data = data.dict()
    user_info = get_user_info_from_token(request)
    # 创建时默认添加创建人、修改者和所属部门
    data['creator_id'] = user_info['id']
    data['modifier'] = user_info['name']
    data['belong_dept'] = user_info['dept']
    query_set = model.objects.create(**data)
    return query_set


def delete(id, model):
    instance = get_object_or_404(model, id=id)
    instance.delete()
    pass


def update(request, id, data, model):
    dict_data = data.dict()
    user_info = get_user_info_from_token(request)
    # 修改时默认添加修改者
    dict_data['modifier'] = user_info['name']
    instance = get_object_or_404(model, id=id)
    for attr, value in dict_data.items():
        setattr(instance, attr, value)
    instance.save()
    return instance


def retrieve(request, model, filters: FuFilters = FuFilters()):
    filters = data_permission(request, filters)
    if filters is not None:
        # 将filters空字符串转换为None
        for attr, value in filters.__dict__.items():
            if getattr(filters, attr) == '':
                setattr(filters, attr, None)
        query_set = model.objects.filter(**filters.dict(exclude_none=True))
    else:
        query_set = model.objects.all()
    return query_set
