<template>
    <v-container>
      <h1>Master Parts Changeover Matrix</h1>
      
      <!-- ตารางแสดง Parts -->
      <v-data-table
        :headers="headers"
        :items="parts"
        class="elevation-1 mb-4"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Parts List</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
            <v-dialog v-model="dialog" max-width="500px">
              <template v-slot:activator="{ on, attrs }">
                <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
                  Add New Part
                </v-btn>
              </template>
              <v-card>
                <v-card-title>
                  <span class="headline">{{ formTitle }}</span>
                </v-card-title>
                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-col cols="12">
                        <v-text-field v-model="editedItem.name" label="Part Name"></v-text-field>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
                  <v-btn color="blue darken-1" text @click="save">Save</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-toolbar>
        </template>
      </v-data-table>
  
      <!-- ตารางแสดง Changeover Matrix -->
      <v-data-table
        :headers="changeoverHeaders"
        :items="changeoverTimes"
        class="elevation-1 mb-4"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Changeover Matrix</v-toolbar-title>
          </v-toolbar>
        </template>
      </v-data-table>
  
      <!-- ปุ่มสำหรับ Import/Export Excel -->
      <v-btn color="primary" @click="triggerExcelImport" class="mr-2">Import Excel</v-btn>
      <v-btn color="secondary" @click="exportExcel">Export Excel</v-btn>
      
      <!-- Input file ซ่อนไว้สำหรับ Import Excel -->
      <input
        type="file"
        ref="excelImporter"
        style="display: none"
        @change="importExcel"
        accept=".xlsx, .xls"
      >
    </v-container>
  </template>
  
  <script>
  import api from '@/services/api';
  
  export default {
    name: 'HomePage',
    data: () => ({
      dialog: false,
      headers: [
        { text: 'Part ID', value: 'id' },
        { text: 'Part Name', value: 'name' },
        { text: 'Actions', value: 'actions', sortable: false }
      ],
      changeoverHeaders: [
        { text: 'From Part', value: 'from_part_id' },
        { text: 'To Part', value: 'to_part_id' },
        { text: 'Time (minutes)', value: 'time' }
      ],
      parts: [],
      changeoverTimes: [],
      editedIndex: -1,
      editedItem: {
        name: ''
      },
      defaultItem: {
        name: ''
      }
    }),
  
    computed: {
      formTitle() {
        return this.editedIndex === -1 ? 'New Part' : 'Edit Part'
      }
    },
  
    watch: {
      dialog(val) {
        val || this.close()
      }
    },
  
    created() {
      this.initialize()
    },
  
    methods: {
      async initialize() {
        try {
          const [partsResponse, changeoverResponse] = await Promise.all([
            api.getParts(),
            api.getChangeoverTimes()
          ]);
          this.parts = partsResponse.data;
          this.changeoverTimes = changeoverResponse.data;
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      },
  
      editItem(item) {
        this.editedIndex = this.parts.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },
  
      deleteItem(item) {
        const index = this.parts.indexOf(item)
        confirm('Are you sure you want to delete this item?') && this.parts.splice(index, 1)
      },
  
      close() {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },
  
      async save() {
        if (this.editedIndex > -1) {
          Object.assign(this.parts[this.editedIndex], this.editedItem)
        } else {
          try {
            const response = await api.createPart(this.editedItem);
            this.parts.push(response.data);
          } catch (error) {
            console.error('Error creating part:', error);
          }
        }
        this.close()
      },
  
      triggerExcelImport() {
        this.$refs.excelImporter.click();
      },
  
      async importExcel(event) {
        const file = event.target.files[0];
        if (!file) return;
  
        const formData = new FormData();
        formData.append('file', file);
  
        try {
          await api.importExcel(formData);
          // Refresh data after import
          this.initialize();
        } catch (error) {
          console.error('Error importing Excel:', error);
        }
      },
  
      async exportExcel() {
        try {
          const response = await api.exportExcel();
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'parts_changeover_data.xlsx');
          document.body.appendChild(link);
          link.click();
        } catch (error) {
          console.error('Error exporting Excel:', error);
        }
      }
    }
  }
  </script>