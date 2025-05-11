<script setup>
import { UsersIcon, EyeIcon } from '@heroicons/vue/24/outline'
import IconGasStation from "@/assets/icons/IconGasStation.vue"
import IconWheel from "@/assets/icons/IconWheel.vue";
import { ref, computed } from 'vue'

const searchQuery = ref('')

const products = [
  {
    id: 1,
    name: 'Basic Tee',
    href: '#',
    imageSrc: '/src/assets/images/carroteste.png',
    imageAlt: "veículo",
    price: '$35',
    color: 'Black',
    plate: 'AA - 12 - BQ',
    type: 'Citadino',
  },
  {
    id: 2,
    name: 'Modern Shirt',
    href: '#',
    imageSrc: 'https://tailwindcss.com/plus-assets/img/ecommerce-images/product-page-01-related-product-02.jpg',
    imageAlt: "Front of men's Modern Shirt in gray.",
    price: '$42',
    color: 'Gray',
    plate: 'BB - 34 - ZX',
    type: 'SUV',
  },
  {
    id: 2,
    name: 'Modern Shirt',
    href: '#',
    imageSrc: 'https://tailwindcss.com/plus-assets/img/ecommerce-images/product-page-01-related-product-02.jpg',
    imageAlt: "Front of men's Modern Shirt in gray.",
    price: '$42',
    color: 'Gray',
    plate: 'BB - 34 - ZX',
    type: 'SUV',
  },
  {
    id: 2,
    name: 'Modern Shirt',
    href: '#',
    imageSrc: 'https://tailwindcss.com/plus-assets/img/ecommerce-images/product-page-01-related-product-02.jpg',
    imageAlt: "Front of men's Modern Shirt in gray.",
    price: '$42',
    color: 'Gray',
    plate: 'BB - 34 - ZX',
    type: 'SUV',
  },
  {
    id: 2,
    name: 'Modern Shirt',
    href: '#',
    imageSrc: 'https://tailwindcss.com/plus-assets/img/ecommerce-images/product-page-01-related-product-02.jpg',
    imageAlt: "Front of men's Modern Shirt in gray.",
    price: '$42',
    color: 'Gray',
    plate: 'BB - 34 - ZX',
    type: 'SUV',
  },
]

const filteredProducts = computed(() => {
  const query = searchQuery.value.toLowerCase()
  return products.filter(product =>
      product.name.toLowerCase().includes(query) ||
      product.color.toLowerCase().includes(query) ||
      product.plate.toLowerCase().includes(query) ||
      product.type.toLowerCase().includes(query)
  )
})
</script>

<template>
  <!-- Search -->
  <div class="relative">
    <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
      <svg class="w-4 h-4 text-gray-900" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
           viewBox="0 0 20 20">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
      </svg>
    </div>
    <input v-model="searchQuery" type="text" id="table-search-users"
           class="block p-2 ps-10 text-sm rounded-lg w-80 bg-transparent border-extra-soft-orange hover:border-soft-orange focus:ring-soft-orange placeholder-gray-500 text-gray-900"
           placeholder="Pesquisar veículos" />
  </div>

  <!-- Grid -->
  <div class="mt-10 max-h-[700px] overflow-y-auto pr-2">
    <div class=" grid gap-x-16 gap-y-20 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 ">
      <div v-for="product in filteredProducts" :key="product.id" class="group relative p-4 rounded-lg shadow hover:shadow-md border border-gray-100">
        <div class="mb-2">
          <div class="flex justify-between items-center">
            <h2 class="text-xl font-bold text-gray-900">{{ product.plate }}</h2>
            <button type="button"
                    class="inline-flex items-center rounded-md bg-extra-soft-orange px-3 py-2 text-sm font-semibold text-gray-900 shadow-xs hover:bg-soft-orange duration-300">
              <EyeIcon class="mr-1.5 -ml-0.5 size-5" aria-hidden="true" />
              Visualizar
            </button>
          </div>
          <span class="text-gray-400">{{ product.type }}</span>
        </div>

        <div>
          <img src="../assets/img/carroteste.png" :alt="product.imageAlt"
               class="aspect-square w-full object-contain rounded-md bg-gradient-to-t from-background-orange to-orange-50 group-hover:opacity-75 lg:aspect-auto lg:h-80" />
        </div>

        <div class="mt-4 space-y-2">
          <div class="flex items-center space-x-2">
            <UsersIcon class="w-6 h-6 " />
            <span>4</span>
          </div>
          <div class="flex items-center space-x-2">
            <IconGasStation :size="24" />
            <span>360 kw</span>
          </div>
          <div class="flex items-center space-x-2">
            <IconWheel :size="24" />
            <span>Automático</span>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>
