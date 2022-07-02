<template>
  <div>
    <BasicTable @register="registerTable">
      <template #tableTitle>
        <a-button type="primary" v-auth="['dict:add']" @click="handleCreate"> 新增 </a-button>
      </template>
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              type: 'button',
              icon: 'clarity:note-edit-line',
              color: 'primary',
              tooltip: '编辑',
              onClick: handleEdit.bind(null, record),
              auth: ['dict:update'],
            },
            {
              icon: 'ant-design:delete-outlined',
              type: 'button',
              color: 'error',
              tooltip: '删除',
              placement: 'left',
              popConfirm: {
                title: '是否确认删除',
                confirm: handleDelete.bind(null, record.id),
              },
              auth: ['dict:delete'],
            },
            {
              type: 'button',
              color: 'warning',
              tooltip: '字典配置',
              icon: 'ant-design:plus-square-outlined',
              onClick: addDictItem.bind(null, record.id),
              auth: ['dict:update'],
            },
          ]"
        />
      </template>
    </BasicTable>
    <DictDrawer @register="registerDrawer" @success="handleSuccess" />
    <AddDictItem @register="registerAddDictItemDrawer" />
  </div>
</template>
<script lang="ts">
  import { defineComponent } from 'vue';

  import { BasicTable, useTable, TableAction } from '/@/components/Table';

  import { useDrawer } from '/@/components/Drawer';
  import DictDrawer from './DictDrawer.vue';
  import AddDictItem from './dict_item/index.vue';

  import { deleteItem, getList } from './dict.api';
  import { columns, searchFormSchema } from './dict.data';

  export default defineComponent({
    name: 'DataDict',
    components: { BasicTable, DictDrawer, TableAction, AddDictItem },
    setup() {
      const [registerDrawer, { openDrawer }] = useDrawer();
      const [registerAddDictItemDrawer, { openDrawer: openAddDictItemDrawer }] = useDrawer();

      const [registerTable, { reload }] = useTable({
        api: getList,
        columns,
        formConfig: {
          labelWidth: 80,
          schemas: searchFormSchema,
        },
        useSearchForm: true,
        showTableSetting: true,
        tableSetting: { fullScreen: true },
        bordered: true,
        showIndexColumn: false,
        actionColumn: {
          width: 150,
          title: '操作',
          dataIndex: 'action',
          slots: { customRender: 'action' },
          fixed: undefined,
        },
      });

      function handleCreate() {
        openDrawer(true, {
          isUpdate: false,
        });
      }

      function handleEdit(record: Recordable) {
        openDrawer(true, {
          record,
          isUpdate: true,
        });
      }

      function addDictItem(id: number) {
        openAddDictItemDrawer(true, {
          id,
        });
      }

      async function handleDelete(id: number) {
        await deleteItem(id);
        await reload();
      }

      function handleSuccess() {
        reload();
      }

      return {
        registerTable,
        registerDrawer,
        registerAddDictItemDrawer,
        handleCreate,
        handleEdit,
        handleDelete,
        handleSuccess,
        addDictItem,
      };
    },
  });
</script>
