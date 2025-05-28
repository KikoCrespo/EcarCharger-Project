<template>
    <div v-if="show" class="fixed inset-0 bg-gray-500/75 transition-opacity flex items-center justify-center z-50">
        <div class=" flex flex-col lg:flex-row gap-10 bg-white p-6 rounded-lg shadow-lg w-full max-w-[80vw] relative">
            <button @click="fecharModal">
                <XMarkIcon class="h-6 w-6 absolute top-4 right-4 text-gray-500 hover:text-gray-700 transition-colors duration-200" />
            </button>
            <div class=" w-full w-1/2 flex items-center justify-center h-[40vh] mb-4 mt-6">
                <img src="../assets/img/carroteste.png" :src="vehicle.v_imagem" alt="Imagem do Veículo"
                    class="w-full h-full object-cover object-contain bg-gradient-to-t from-extra-soft-orange to-orange-50">
            </div>
            <div class=" w-full w-1/2  grid grid-cols-1 md:grid-cols-2 gap-5 mb-3 p-4 mt-6 max-h-[60vh] md:max-h-[70vh] lg:max-h-[60vh]">
                <div class=" mb-2 border-b border-extra-soft-orange">
                    <label for="marca" class="block text-sm text-gray-600 mb-1.5 ">Marca</label>
                    <label for="marca">{{ vehicle.v_marca }}</label>
                </div>

                <div class=" mb-2 border-b border-extra-soft-orange">
                    <label for="modelo" class="block text-sm text-gray-600 mb-1.5">Modelo</label>
                    <label for="modelo">{{ vehicle.v_modelo }}</label>
                </div>
                <div class=" mb-2 border-b border-extra-soft-orange">

                    <label for="matricula" class="block text-sm text-gray-600 mb-1.5">Matrícula</label>
                    <label for="matricula">{{ vehicle.v_matricula }}</label>
                </div>

                <div class=" mb-2 border-b border-extra-soft-orange">
                    <label for="anoMatricula" class="block text-sm text-gray-600 mb-1.5">Ano de Matrícula</label>
                    <label for="anoMatricula">{{ vehicle.v_ano_matricula }}</label>
                </div>

                <div class=" mb-2 border-b border-extra-soft-orange">
                    <label for="categoria" class="block text-sm text-gray-600 mb-1.5">Categoria</label>
                    <label for="categoria">{{ vehicle.v_categoria_display }}</label>
                </div>
                <div class=" mb-2 border-b border-extra-soft-orange">
                    <label for="potencia" class="block text-sm text-gray-600 mb-1.5">Celindrada</label>
                    <label for="potencia">{{ vehicle.v_potencia }}</label>
                </div>

                <div class=" mb-2 border-b border-extra-soft-orange">
                    <label for="transmissao" class="block text-sm text-gray-600 mb-1.5">Transmissão</label>
                    <label for="transmissao">{{ vehicle.v_transmissao }}</label>
                </div>

                <div class=" mb-2 border-b border-extra-soft-orange">
                    <label for="combustivel" class="block text-sm text-gray-600 mb-1.5">Combustível</label>
                    <label for="combustivel">{{ vehicle.v_combustivel }}</label>
                </div>

                <div class=" mb-2 border-b border-extra-soft-orange">
                    <label for="assentos" class="block text-sm text-gray-600 mb-1.5">Numero de lugares</label>
                    <label for="assentos">{{ vehicle.v_assentos }}</label>
                </div>

                <div class=" mb-2 border-b border-extra-soft-orange">
                    <label for="cor" class="block text-sm text-gray-600 mb-1.5">Cor</label>
                    <label for="cor">{{ vehicle.v_cor }}</label>
                </div>

                <div class=" mb-2 border-b border-extra-soft-orange">
                    <label for="emissoes" class="block text-sm text-gray-600 mb-1.5">Emissões de CO2</label>
                    <label for="emissoes">{{ vehicle.v_emissoes }}</label>
                </div>

                <div class=" mb-2 border-b border-extra-soft-orange">
                    <label for="estado" class="block text-sm text-gray-600 mb-1.5">Estado</label>
                    <label for="estado">{{ getv_estadoText(vehicle.v_estado) }}</label>
                </div>

                <div class=" mb-2 border-b border-extra-soft-orange">
                    <label for="quilometragem" class="block text-sm text-gray-600 mb-1.5">Quilometragem</label>
                    <label for="quilometragem">{{ vehicle.v_quilometros }}</label>
                </div>

            </div>

        </div>

    </div>
</template>

<script setup>
import { XMarkIcon } from '@heroicons/vue/20/solid'

const props = defineProps({
    show: Boolean,
    vehicle: Object
});

const getv_estadoText = (estado) => {
    switch (estado) {
        case 1: return 'Disponível';
        case 2: return 'Em Uso';
        case 3: return 'Manutenção';
        default: return estado;
    }
};

const emit = defineEmits(['update:show']);

function fecharModal() {
    emit('update:show', false);
}
</script>