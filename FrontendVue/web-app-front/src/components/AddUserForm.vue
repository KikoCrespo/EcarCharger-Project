<template>
  <form>
    <div class="space-y-12">
      <div class="border-b border-gray-900/10 pb-12">
        <h2 class="text-base/7 font-semibold text-gray-900">Novo utilizador</h2>
        <p class="mt-1 text-sm/6 text-gray-600">descrição</p>

        <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6 ">
          <div class="sm:col-span-3">
            <label for="first-name" class="block text-sm/6 font-medium text-gray-900">Nome</label>
            <div class="mt-2">
              <input type="text" name="first-name" id="first-name" autocomplete="given-name" class="w-full mt-1 px-4 py-3 text-sm border-b border-extra-soft-orange focus:border-soft-orange focus:outline-hidden" />
            </div>
          </div>

          <div class="sm:col-span-3">
            <label for="last-name" class="block text-sm/6 font-medium text-gray-900">Apelido</label>
            <div class="mt-2">
              <input type="text" name="last-name" id="last-name" autocomplete="family-name" class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6" />
            </div>
          </div>

          <div class="sm:col-span-3">
            <label for="username" class="block text-sm/6 font-medium text-gray-900">Email</label>
            <div class="mt-2">
              <div class="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600">
                <div class="shrink-0 mr-1 text-base text-gray-500 select-none sm:text-sm/6">entidade.com/</div>
                <input type="text" name="username" id="username" class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6" placeholder="utilizador" />
              </div>
            </div>
          </div>

          <div class="sm:col-span-3">
            <label for="password" class="block text-sm/6 font-medium text-gray-900">Password padrão</label>
            <div class="mt-2">
              <input type="password" name="password" id="password" autocomplete="family-name" class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6" />
            </div>
          </div>
          <div class="sm:col-span-3">
            <label class="inline-flex items-center cursor-pointer">
              <input type="checkbox" value="" class="sr-only peer">
              <div class="relative w-11 h-6 bg-gray-200  rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all  peer-checked:bg-soft-orange"></div>
              <span class="ms-3 text-sm font-medium text-gray-900 ">Admin</span>
            </label>
          </div>

          <div class="sm:col-span-3">
            <label for="country" class="block text-sm/6 font-medium text-gray-900">Departamento</label>
            <div class="mt-2 grid grid-cols-1">
              <select id="country" name="country" autocomplete="country-name" class="col-start-1 row-start-1 w-full appearance-none rounded-md bg-white py-1.5 pr-8 pl-3 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">
                <option>Utilizador</option>
                <option>Admin</option>
              </select>
              <ChevronDownIcon class="pointer-events-none col-start-1 row-start-1 mr-2 size-5 self-center justify-self-end text-gray-500 sm:size-4" aria-hidden="true" />
            </div>
          </div>


          <div class="col-span-full">
            <label for="photo" class="block text-sm/6 font-medium text-gray-900">Photo</label>
            <div class="mt-2 flex items-center gap-x-3">
              <UserCircleIcon class="size-12 text-gray-300" aria-hidden="true" />
              <button type="button" class="rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 shadow-xs ring-1 ring-gray-300 ring-inset hover:bg-gray-50">Change</button>
            </div>
          </div>
        </div>
      </div>

    </div>

    <div class="mt-6 flex items-center justify-end gap-x-6">
      <button type="button" class="text-sm/6 font-semibold text-gray-900">Cancel</button>
      <button type="submit" class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Save</button>
    </div>
  </form>
</template>

<script setup>
import { PhotoIcon, UserCircleIcon } from '@heroicons/vue/24/solid'
import { ChevronDownIcon } from '@heroicons/vue/16/solid'
</script>