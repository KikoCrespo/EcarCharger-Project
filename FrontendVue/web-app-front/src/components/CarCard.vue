<script setup>
import { UsersIcon } from '@heroicons/vue/24/outline'


const products = [
  {
    id: 1,
    name: 'Basic Tee',
    href: '#',
    imageSrc: 'https://tailwindcss.com/plus-assets/img/ecommerce-images/product-page-01-related-product-01.jpg',
    imageAlt: "Front of men's Basic Tee in black.",
    price: '$35',
    color: 'Black',
  },
  {
    id: 1,
    name: 'Basic Tee',
    href: '#',
    imageSrc: 'https://tailwindcss.com/plus-assets/img/ecommerce-images/product-page-01-related-product-01.jpg',
    imageAlt: "Front of men's Basic Tee in black.",
    price: '$35',
    color: 'Black',
  },
  // More products...
]
</script>

<template>

    <div class="">
      <h2 class="text-xl font-bold  text-gray-900">AA - 12 - BQ</h2>
      <span class="text-gray-400">citadino</span>

      <div class="">
        <div v-for="product in products" :key="product.id" class="group relative grid grid-cols-3 gap-4">
          <div class="col-span-2">
            <img :src="product.imageSrc" :alt="product.imageAlt" class="aspect-square w-full rounded-md bg-gray-200 object-cover group-hover:opacity-75 lg:aspect-auto lg:h-80" />
            <div class="mt-4 flex justify-between">
              <div>
                <h3 class="text-sm text-gray-700">
                  <a :href="product.href">
                    <span aria-hidden="true" class="absolute inset-0" />
                    {{ product.name }}
                  </a>
                </h3>
                <p class="mt-1 text-sm text-gray-500">{{ product.color }}</p>
              </div>
              <p class="text-sm font-medium text-gray-900">{{ product.price }}</p>
            </div>
          </div>
          <div class="">
            <div class="flex">
              <UsersIcon class="mr-1.5 -ml-0.5 size-5" aria-hidden="true" />
              <span class=""> Adicionar utilizador</span>
            </div>
            <div class="flex">
              <UsersIcon class="mr-1.5 -ml-0.5 size-5" aria-hidden="true" />
              <span class=""> Adicionar utilizador</span>
            </div>
          </div>
        </div>

      </div>
    </div>
</template>
