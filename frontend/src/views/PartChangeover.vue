<template>
    <v-container>
      <h1>Master Parts Changeover</h1>
  
      <!-- ตารางแสดง Parts -->
      <v-data-table :headers="headers" :items="parts" class="elevation-1 mb-4">
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
  
  
    </v-container>
  </template>
  
  <script>
  
  export default {
    name: 'PartChangeOver',
    data: () => ({
      dialog: false,
      
    }),
  
    computed: {
     
    },
  
    watch: {
     
    },
  
    created() {
    },
  
    methods: {
      
    }
  }
  </script>