<template>
  <div class="max-w-[80vw] max-h-[80vh] mx-auto p-5">
    <!-- Registration Form -->
    <div class="bg-white rounded-lg shadow">
      <form @submit.prevent="submitForm" class="flex flex-col lg:flex-row gap-0">
        <!-- Informações do Veículo -->
        <div class="w-full w-1/2  p-6 border-r border-extra-soft-orange mt-2 mb-2">
          <h2 class="text-lg font-medium text-gray-800 mb-5 ">Informações do Veículo</h2>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-5">
            <div>
              <label for="plate" class="block text-sm text-gray-600 mb-1.5">Matrícula*</label>
              <input type="text" id="plate" v-model="form.c_matricula" placeholder="AA-00-BB" required
                class="w-full px-3 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange" />
              <span v-if="formErrors.c_matricula" class="text-red-500 text-sm">{{ formErrors.c_matricula }} </span>
            </div>

            <div>
              <label for="vin" class="block text-sm text-gray-600 mb-1.5">Número de Chassis (VIN)*</label>
              <input type="text" id="vin" v-model="form.c_chassis" placeholder="WBA12345678901234" required
                class="w-full px-3 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange" />
              <span v-if="formErrors.c_chassis" class="text-red-500 text-sm">{{ formErrors.c_chassis }} </span>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-5">
            <div>
              <label for="brand" class="block text-sm text-gray-600 mb-1.5">Marca*</label>
              <select id="brand" v-model="form.c_marca" required
                class="w-full px-3 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange">
                <option value="" disabled selected>Selecione uma marca</option>
                <option value="Toyota">Toyota</option>
                <option value="Renault">Renault</option>
                <option value="Mercedes">Mercedes</option>
                <option value="BMW">BMW</option>
                <option value="Audi">Audi</option>
                <option value="Ford">Ford</option>
                <option value="Volkswagen">Volkswagen</option>
              </select>
              <span v-if="formErrors.c_marca" class="text-red-500 text-sm">{{ formErrors.c_marca }} </span>
            </div>

            <div>
              <label for="model" class="block text-sm text-gray-600 mb-1.5">Modelo*</label>
              <input type="text" id="model" v-model="form.c_modelo" placeholder="Ex: Corolla" required
                class="w-full px-3 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange" />
              <span v-if="formErrors.c_modelo" class="text-red-500 text-sm">{{ formErrors.c_modelo }} </span>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-5">
            <div>
              <label for="yearMonth" class="block text-sm text-gray-600 mb-1.5">Ano da Matricula [Ano e Mês]*</label>
              <div class="flex gap-3">
                <select v-model="form.c_registo_ano" required
                  class="w-full px-3 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange">
                  <option value="" disabled selected>Ano</option>
                  <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
                </select>

                <select v-model="form.c_registo_mes" required
                  class="w-full px-3 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange">
                  <option value="" disabled selected>Mês</option>
                  <option v-for="(mes, index) in meses" :key="index" :value="index + 1">{{ mes }}</option>
                </select>
              </div>
              <span v-if="formErrors.c_registo_ano || formErrors.c_registo_mes" class="text-red-500 text-sm"> Campo
                obrigatório </span>
            </div>

            <div>
              <label for="color" class="block text-sm text-gray-600 mb-1.5">Cor</label>
              <input type="text" id="color" v-model="form.c_cor" placeholder="Ex: Branco"
                class="w-full px-3 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange" />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div>
              <label for="category" class="block text-sm text-gray-600 mb-1.5">Categoria*</label>
              <select id="category" v-model="form.c_categoria" required
                class="w-full px-3 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange">
                <option value="" disabled selected>Selecione uma categoria</option>
                <option :value="1">Sedan</option>
                <option :value="2">Citadino</option>
                <option :value="3">SUV</option>
                <option :value="4">Comercial</option>
                <option :value="5">Utilitário</option>
              </select>
              <span v-if="formErrors.c_categoria" class="text-red-500 text-sm">{{ formErrors.c_categoria }} </span>
            </div>

            <div>
              <label for="fuel" class="block text-sm text-gray-600 mb-1.5">Combustível*</label>
              <select id="fuel" v-model="form.c_combustivel" required
                class="w-full px-3 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange">
                <option value="" disabled selected>Selecione o combustível</option>
                <option value="Gasolina">Gasolina</option>
                <option value="Diesel">Diesel</option>
                <option value="Híbrido">Híbrido</option>
                <option value="Elétrico">Elétrico</option>
                <option value="GPL">GPL</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Informações Adicionais -->
        <div class=" w-full w-1/2 ml-0 p-6 mt-2 mb-2">
          <h2 class="text-lg font-medium text-gray-800 mb-5">Informações Adicionais</h2>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-5">
            <div>
              <label for="year" class="block text-sm text-gray-600 mb-1.5">Numero de lugares*</label>
              <input type="number" id="assents" v-model="form.c_lugares" min="1" required
                class="w-full px-3 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange" />
              <span v-if="formErrors.c_lugares" class="text-red-500 text-sm">{{ formErrors.c_lugares }} </span>
            </div>
            <div>
              <label for="purchaseDate" class="block text-sm text-gray-600 mb-1.5">Data de Aquisição</label>
              <input type="date" id="purchaseDate" v-model="form.c_data_aquisicao" required
                class="w-full px-3 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange" />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-5">
            <div>
              <label for="transmissao" class="block text-sm text-gray-600 mb-1.5">Transmissão*</label>
              <select id="transmissao" v-model="form.c_transmissao" required
                class="w-full px-3 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange">
                <option value="" disabled selected>Tipo de Transmissão</option>
                <option value="Manual">Manual</option>
                <option value="Automatico">Automática</option>
              </select>
              <span v-if="formErrors.c_transmissao" class="text-red-500 text-sm">{{ formErrors.c_transmissao }} </span>
            </div>
            <div>
              <label for="km" class="block text-sm text-gray-600 mb-1.5">Quilometragem*</label>
              <input type="number" id="km" v-model="form.c_quilometros" min="0"
                class="w-full px-3 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange" />
              <span v-if="formErrors.c_km" class="text-red-500 text-sm">{{ formErrors.c_km }} </span>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-5">
            <div>
              <label for="emissions" class="block text-sm text-gray-600 mb-1.5">Emissões CO2 [g/km]</label>
              <input type="number" id="emissions" v-model="form.c_emissoes" min="0"
                class="w-full px-3 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange" />
            </div>
            <div>
              <!-- Botão para abrir modal -->
              <button @click="openModal = true"
                class="mt-7 px-3 py-2 bg-extra-soft-orange hover:bg-soft-orange duration-300  text-gray-900 rounded-lg flex items-center justify-center gap-1">
                + Documentos
              </button>

              <!-- Lista de documentos já adicionados -->
              <ul class="mt-4 space-y-2">
                <li v-for="(doc, index) in documentos" :key="index">
                  <span class="font-medium"> {{ doc.tipo }}</span> - {{ doc.titulo }}
                </li>
              </ul>

              <!-- Modal -->
              <div v-if="openModal"
                class="fixed inset-0 bg-gray-500/75 transition-opacity flex items-center justify-center z-50">
                <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-md relative">
                  <h2 class="text-lg font-semibold mb-4">Adicionar Documento</h2>

                  <label for="tipo" class="block text-sm text-gray-600 mb-1.5">Tipo*</label>
                  <select id="tipo" v-model="tipoDocumento" required
                    class="w-full px-3 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange">
                    <option value="" disabled selected>Selecione o tipo de documento</option>
                    <option value="Seguro">Seguro</option>
                    <option value="Inspeção">Inspeção</option>
                    <option value="IUC">IUC</option>
                    <option value="Outros">Outros</option>
                  </select>

                  <label class="block text-sm text-gray-600 mb-1.5 mt-2">Título*</label>
                  <input v-model="novoTitulo" type="text" placeholder="Ex: Seguro" required
                    class="w-full border px-3 py-2 rounded-md mb-4 border border-gray-300 focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange" />

                  <label for="DateDocument" class="block text-sm text-gray-600 mb-1.5">Data do documento*</label>
                  <input type="date" id="DateDocument" v-model="dataNovoDocumento" required
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange" />

                  <label for="ExpDateDocument" class="block text-sm text-gray-600 mb-1.5">Data de Validade</label>
                  <input type="date" id="ExpDateDocument" v-model="dataValidadeNovoDocumento"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange" />

                  <label class="block text-sm text-gray-600 mb-1.5 mt-2">Ficheiro*</label>
                  <input type="file" accept=".pdf,.jpg,.jpeg,.png" @change="handleFileChange"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md bg-transparent file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-transparent file:text-soft-orange hover:file:text-extra-soft-orange focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange hover:file:bg-transparent" />
                  <div class="flex justify-end gap-2">
                    <button @click="adicionarDocumento"
                      class="mt-4 px-3 py-2 bg-extra-soft-orange hover:bg-soft-orange duration-300  font-semibold text-gray-900 py-2 rounded-lg">
                      Adicionar
                    </button>
                    <button @click="fecharModal"
                      class="mt-4 bg-gray-100 hover:bg-gray-200 text-gray-800 duration-300 px-3 py-2 rounded-lg">
                      Cancelar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-5">
            <div>
              <label for="power" class="block text-sm text-gray-600 mb-1.5">Potencia</label>
              <input type="number" id="power" v-model="form.c_potencia" min="0"
                class="w-full px-3 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange" />
              <span v-if="formErrors.c_potencia" class="text-red-500 text-sm">{{ formErrors.c_potencia }} </span>
            </div>
          </div>

          <div class="mb-0">
            <label for="notes" class="block text-sm text-gray-600 mb-1.5">Notas</label>
            <textarea id="notes" v-model="form.c_notas" rows="3" placeholder="Informações adicionais sobre o veículo"
              class="w-full px-3 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-extra-soft-orange focus:border-soft-orange resize-y"></textarea>
          </div>
        </div>


        
      </form>
      <!-- Botões de Ação -->
        <div class="flex justify-end gap-3 p-6 bg-gray-50 rounded-b-lg">
          <button @click="openModalConfirm()"
            class="px-3 py-2 bg-extra-soft-orange hover:bg-soft-orange duration-300  text-gray-900  rounded-lg flex items-center justify-center gap-1">
            Registar Veículo
          </button>
        </div>
    </div>
  </div>

  <ConfirmModal :open="showModal" :title="modalTitle" :message="modalMessage" :action="modalAction" @close="closeModal"
    @confirm="handleConfirm" />
</template>



<script setup>
import { onMounted, ref, defineProps, computed } from 'vue'
import { UserCircleIcon, PencilIcon } from '@heroicons/vue/24/outline'
import api from '@/interceptors/axiosInterceptor'
import ConfirmModal from '@/components/ConfirmModal.vue'

const currentYear = new Date().getFullYear();
const years = Array.from({ length: 50 }, (_, i) => currentYear - i);
const meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];

const openModal = ref(false)
const documentos = ref([])

const novoTitulo = ref('')
const novoFicheiro = ref(null)
const dataNovoDocumento = ref('')
const tipoDocumento = ref('')
const dataValidadeNovoDocumento = ref('')


const showModal = ref(false);
const modalTitle = ref('');
const modalMessage = ref('');
const modalAction = ref('');

function openModalConfirm() {
  modalTitle.value = 'Confirmar Registo de veiculo'
  modalMessage.value = 'Tens a certeza que queres registar o veiculo com a matricula ' + form.value.c_matricula + '?'
  modalAction.value = 'Registar'
  showModal.value = true
}
function closeModal() {
  showModal.value = false
}

function handleConfirm() {
  submitForm();
  showModal.value = false;
}




const form = ref({
  c_matricula: '',
  c_chassis: '',
  c_marca: '',
  c_modelo: '',
  c_cor: '',
  c_categoria: '',
  c_combustivel: '',
  c_lugares: '',
  c_data_aquisicao: '',
  c_registo_ano: '',
  c_registo_mes: '',
  c_transmissao: '',
  c_quilometros: '',
  c_emissoes: '',
  c_potencia: '',
  c_notas: '',
});

const camposObrigatorios = [
  'c_matricula',
  'c_chassis',
  'c_marca',
  'c_modelo',
  'c_categoria',
  'c_combustivel',
  'c_lugares',
  'c_registo_ano',
  'c_registo_mes',
  'c_transmissao',
  'c_potencia',
  'c_quilometros',
];

const formErrors = ref({
  c_matricula: '',
  c_chassis: '',
  c_marca: '',
  c_modelo: '',
  c_cor: '',
  c_categoria: '',
  c_combustivel: '',
  c_lugares: '',
  c_data_aquisicao: '',
  c_data_registo: '',
  c_transmissao: '',
  c_quilometros: '',
  c_emissoes: '',
  c_notas: '',
  c_potencia: '',
  c_registo_ano: '',
  c_registo_mes: '',
});



const submitForm = async () => {


  const formData = new FormData();

  resetFormErrors();

  let isValid = true;

  // Validação dos campos
  camposObrigatorios.forEach(campo => {
    if (!form.value[campo]) {
      formErrors.value[campo] = 'Campo obrigatório';
      isValid = false;
    }
  });

  if (!isValid) {
    return;
  }

  if (!/^[A-Z]{2}-\d{2}-[A-Z]{2}$/.test(form.value.c_matricula)) {
    formErrors.value.c_matricula = 'Formato inválido (ex: AA-00-BB)';
    isValid = false;
  }

  if (!/^[A-HJ-NPR-Z0-9]{17}$/.test(form.value.c_chassis)) {
    formErrors.value.c_chassis = 'VIN inválido (17 caracteres)';
    isValid = false;
  }


  // Adiciona os campos do formulário
  for (const key in form.value) {
    formData.append(key, form.value[key]);
  }

  // Adiciona os documentos com os ficheiros
  documentos.value.forEach((doc, index) => {
    formData.append(`documentos[${index}][tipo]`, doc.tipo);
    formData.append(`documentos[${index}][titulo]`, doc.titulo);
    formData.append(`documentos[${index}][data]`, doc.data);
    formData.append(`documentos[${index}][validade]`, doc.dataValidade || '');
    formData.append(`documentos[${index}][ficheiro]`, doc.ficheiro);
  });

  try {
    const response = await api.post('/frota/adicionar-veiculo/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    // Se o envio for bem-sucedido, redireciona ou exibe uma mensagem de sucesso
    // Redirecionar ou exibir mensagem de sucesso

    console.log('Formulário de registo de viatura enviado com sucesso', response.data);
  } catch (error) {
    if (error.response && error.response.data) {
      const errors = error.response.data;
      for (const key in errors) {
        if (formErrors.value.hasOwnProperty(key)) {
          formErrors.value[key] = errors[key];
        }
      }
    } else {

      console.error('Erro ao enviar o formulário de registo de viatura:', error);
    }
    console.error('Erro ao enviar o formulário de registo de viatura:', error);
  }
};



function handleFileChange(event) {
  const file = event.target.files[0]
  if (file) {
    novoFicheiro.value = file
  }
}

function adicionarDocumento() {
  if (novoTitulo.value && novoFicheiro.value && tipoDocumento.value) {
    documentos.value.push({
      tipo: tipoDocumento.value,
      titulo: novoTitulo.value,
      ficheiro: novoFicheiro.value,
      data: dataNovoDocumento.value,
      dataValidade: dataValidadeNovoDocumento.value
    })
    novoTitulo.value = ''
    novoFicheiro.value = null
    dataNovoDocumento.value = ''
    tipoDocumento.value = ''
    dataValidadeNovoDocumento.value = ''
    // Fechar o modal
    openModal.value = false
  } else {
    alert('Por favor, preencha os campos obrigatórios [*]')
  }
}

const resetFormErrors = () => {
  Object.keys(formErrors.value).forEach(key => {
    formErrors.value[key] = '';
  });
};

function fecharModal() {
  novoTitulo.value = ''
  novoFicheiro.value = null
  openModal.value = false
}
</script>
