<template>
    <div class="w-64 bg-orange-200 text-white p-4">
        <h2 class="text-2xl font-semibold mb-6">HMV</h2>
        <ul>
            <li class="mb-4">
                <router-link to="/home" class="text-white hover:text-gray-300">Home</router-link>
            </li>
            <li class="mb-4">
                <router-link to="/entidades" class="text-white hover:text-gray-300">Entidades</router-link>
                <option value="">adicionar Entidade</option>
            </li>
            <li class="mb-4">
                <router-link to="/registar" class="text-white hover:text-gray-300">Registar Entidade</router-link>
            </li>
        </ul>
    </div>
</template>
