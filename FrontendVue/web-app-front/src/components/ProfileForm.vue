<template>
  <form @submit.prevent="handleSubmit">
    <div class="flex h-auto gap-0 bg-white rounded-md">


      <div class="flex w-1/2 gap-0 ">
        <div class="relative w-full flex items-center justify-center py-8 mt-5 mb-5">
          <button type="button" @click="isEditing = true" class="absolute top-2 left-7 hover:cursor-pointer">
            <PencilIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
          </button>
          <div>
            <label v-if="isEditing" class="cursor-pointer w-full h-full block relative">
              <input type="file" accept="image/*" class="hidden" @change="onFileChange" />
              <div
                class="w-50 h-50 rounded-full overflow-hidden shadow-lg bg-gray-100 flex items-center justify-center hover:w-60 hover:h-60 transition-all duration-300">
                <img v-if="previewUrl" :src="previewUrl" alt="Foto de perfil" class="w-full h-full object-cover" />
                <UserCircleIcon v-else class="w-50 h-50 text-gray-300 hover:w-60 hover:h-60 transition-all duration-300"
                  aria-hidden="true" />
              </div>
            </label>
            <div v-else
              class="w-50 h-50 rounded-full overflow-hidden shadow-lg bg-gray-100 flex items-center justify-center hover:w-60 hover:h-60 transition-all duration-300">
              <img v-if="previewUrl" :src="previewUrl" alt="Foto de perfil" class="w-full h-full object-cover" />
              <UserCircleIcon v-else class="w-50 h-50 text-gray-300 hover:w-60 hover:h-60 transition-all duration-300"
                aria-hidden="true" />
            </div>
          </div>
          <!-- <UserCircleIcon class="w-50 h-50 text-gray-300 shadow-md rounded-full" aria-hidden="true" /> -->
        </div>
      </div>

      <div class="flex w-full justify-center items-center pb-10 pl-5 border-l border-soft-orange mt-5 mb-5 ">
        <div class=" flex-1 w-auto pr-20 mt-5 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
          <div class=" ">
            <h2 class="text-xl font-bold text-gray-900">Meu Perfil</h2>
            <p class="mt-1 text-sm text-gray-600">Atualize as suas informações pessoais.</p>
          </div>
          <div class="grid grid-cols-2 gap-x-6 gap-y-8 sm:col-span-6">
            <div>
              <label for="first-name" class="block text-sm font-medium text-gray-900">Primeiro Nome</label>
              <div class="mt-2">
                <input type="text" name="first-name" id="first-name" autocomplete="given-name" :readonly="!isEditing"
                  :disabled="!isEditing" v-model="form.firstName"
                  class="block w-auto border-0 border-b border-extra-soft-orange  bg-transparent text-gray-900 placeholder:text-gray-400 focus:border-soft-orange focus:outline-none focus:ring-0 duration-300 sm:text-sm" />
              </div>
            </div>

            <div>
              <label for="last-name" class="block text-sm font-medium text-gray-900">Último Nome</label>
              <div class="mt-2">
                <input type="text" name="last-name" id="last-name" autocomplete="family-name" :readonly="!isEditing"
                  :disabled="!isEditing" v-model="form.lastName"
                  class="block w-auto border-0 border-b border-extra-soft-orange  bg-transparent text-gray-900 placeholder:text-gray-400 focus:border-soft-orange focus:outline-none focus:ring-0 duration-300 sm:text-sm" />
              </div>
            </div>
          </div>

          <div class="sm:col-span-4">
            <label for="email" class="block text-sm font-medium text-gray-900">Email</label>
            <div class="mt-2 ">
              <input id="email" name="email" type="email" autocomplete="email" :readonly="!isEditing" :disabled=true
                v-model="form.email"
                class="block w-auto border-0 border-b border-extra-soft-orange  bg-transparent text-gray-900 placeholder:text-gray-400 focus:border-soft-orange focus:outline-none focus:ring-0 duration-300 sm:text-sm" />
            </div>
          </div>

          <div class="sm:col-span-5">
            <label for="departamento" class="block text-sm font-medium text-gray-900">Departamento</label>
            <div class="mt-2">
              <input v-if="!isEditing" type="text" name="departamento" id="departamento" :readonly="!isEditing"
                :disabled="!isEditing" v-model="form.departamento" class="block w-auto border-0 border-b border-extra-soft-orange bg-transparent text-gray-900 placeholder:text-gray-400 focus:border-soft-orange focus:outline-none focus:ring-0 duration-300 sm:text-sm" />
              <select v-else id="departamento" name="departamento" :disabled="!isEditing" v-model="form.departamento"
                class="block w-auto border-0 border-b border-extra-soft-orange bg-transparent text-gray-900 placeholder:text-gray-400 focus:border-soft-orange focus:outline-none focus:ring-0 duration-300 sm:text-sm">
                <option v-if="form.departamento" disabled value="">Selecione um departamento</option>
                <option v-for="dep in departamentos" :key="dep" :value="dep">{{ dep }}</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-x-6 gap-y-8 sm:col-span-6">
            <div>
              <label for="password" class="block text-sm font-medium text-gray-900">Palavra-passe</label>
              <div class="mt-2">
                <input type="password" name="password" id="password" :readonly="!isEditing" :disabled="!isEditing"
                  v-model="form.password"
                  class="block w-auto border-0 border-b border-extra-soft-orange bg-transparent text-gray-900 placeholder:text-gray-400 focus:border-soft-orange focus:outline-none focus:ring-0 duration-300 sm:text-sm" />
              </div>
            </div>

            <div v-if="isEditing">
              <label for="confirm-password" class="block text-sm font-medium text-gray-900">Confirmar
                Palavra-passe</label>
              <div class="mt-2">
                <input type="password" name="confirm-password" id="confirm-password" :readonly="!isEditing"
                  :disabled="!isEditing" v-model="form.passwordConfirm"
                  class="block w-auto border-0 border-b border-extra-soft-orange  bg-transparent text-gray-900 placeholder:text-gray-400 focus:border-soft-orange focus:outline-none focus:ring-0 duration-300 sm:text-sm" />
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <div v-if="isEditing" class="mt-2 flex items-center justify-end gap-x-6">
      <button type="button" @click="cancelEdit"
        class="text-sm font-semibold text-gray-400 hover:text-gray-900">Cancelar</button>
      <button type="submit"
        class="rounded-md bg-extra-soft-orange px-3 py-2 text-sm font-semibold text-gray-400 shadow-sm hover:bg-soft-orange hover:text-black duration-300 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange-200">
        Guardar
      </button>
    </div>
  </form>
</template>

<script setup>
import { onMounted, ref, defineProps, watch } from 'vue'
import { UserCircleIcon, PencilIcon } from '@heroicons/vue/24/outline'
import api from '@/interceptors/axiosInterceptor'

const isEditing = ref(false)
const selectedImage = ref(null)
const previewUrl = ref(null)

const departamentos = [
  'Recursos Humanos',
  'Engenharia',
  'Marketing',
  'Financeiro',
  'TI',
  'Operações'
];

const props = defineProps({
  user_data: {
    type: Object,
    required: true
  }
});

const form = ref({
  firstName: '',
  lastName: '',
  email: '',
  departamento: '',
  password: '',
  passwordConfirm: '',
  foto: ''
});

onMounted(() => {
  if (props.user_data) {
    previewUrl.value = props.user_data.foto_url || '';
    form.value = {
      firstName: props.user_data.first_name || '',
      lastName: props.user_data.last_name || '',
      email: props.user_data.email || '',
      departamento: props.user_data.department || '',
      password: 'Password',
    };
  }
});

watch(() => props.user_data, (newData) => {
  if (newData) {
    form.value = {
      firstName: newData.first_name || '',
      lastName: newData.last_name || '',
      email: newData.email || '',
      departamento: newData.department || '',
      password: ''
    };
  }
},
  { immediate: true }
);

const cancelEdit = () => {
  isEditing.value = false

}


const handleSubmit = () => {
  const token = sessionStorage.getItem('token');
  const formData = new FormData();

  formData.append('first_name', form.value.firstName);
  formData.append('last_name', form.value.lastName);
  formData.append('email', form.value.email);
  formData.append('u_departamento', form.value.departamento);

  if (form.value.password == form.value.passwordConfirm) {
    formData.append('password', form.value.password);
  } else {
    alert('As palavras-passe não coincidem');
    return;
  }

  if (selectedImage.value) {
    formData.append('foto', selectedImage.value);  // <-- importante
  }

  api.put('http://localhost:8000/api/utilizadores/editar/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${token}`
    }
  })
    .then(response => {
      console.log('Dados atualizados com sucesso:', response.data);
      isEditing.value = false;
    })
    .catch(error => {
      console.error('Erro ao atualizar os dados:', error);
    });
};



const handleFileUpload = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    previewUrl.value = e.target.result
  }
  reader.readAsDataURL(file)
}

const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedImage.value = file;
    handleFileUpload(file);
  }
};
</script>
