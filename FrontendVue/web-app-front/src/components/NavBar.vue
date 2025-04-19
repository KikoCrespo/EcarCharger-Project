<template>
    <Disclosure as="nav" class="w-full">
        <div class="flex h-16 items-center justify-between mr-2">
            <div>
                <div class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
                    <div class="hidden sm:ml-6 sm:block">
                        <div>
                            <h1 class="font-semibold text-gray-900">Pedro Silva</h1>
                            <span class="text-sm text-gray-400 font-extralight">Último acesso 24-02-2025 - 14:32</span>
                        </div>
                    </div>
                </div>
            </div>
            <div>
                <!-- Botão de Notificação -->
                <div class="right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
                    <Menu as="div" class="relative ml-3">
                    <div>
                        <MenuButton class="relative rounded-full p-1 text-soft-orange focus:ring-2 focus:ring-soft-orange">
                        <span class="sr-only">Ver notificações</span>
                        <BellIcon class="size-6" />
                        </MenuButton>
                    </div>
        
                    <!-- Dropdown de notificações -->
                    <transition enter-active-class="transition ease-out duration-100" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
                        <MenuItems class="absolute right-0 z-10 mt-2 w-80 max-h-64 overflow-y-auto rounded-md bg-white shadow-lg ring-1 ring-black/5 focus:outline-none">
                        <div class="p-2">
                            <p class="text-gray-700 font-semibold mb-2">Notificações</p>
                            <div v-for="(notification, index) in notifications" :key="index" class="p-2 rounded-md hover:bg-gray-100 cursor-pointer border-b border-gray-100">
                            <p class="text-sm text-gray-800">{{ notification.title }}</p>
                            <p class="text-xs text-gray-500">{{ notification.time }}</p>
                            </div>
                        </div>
                        </MenuItems>
                    </transition>
                    </Menu>
        
                    <!-- (Opcional) Avatar de Perfil -->
                    <img class="size-8 ml-4 rounded-full" src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="User Avatar" />
                </div>
            </div>
          
        </div>
    </Disclosure>
  </template>
  
  <script setup>
  import { Disclosure, DisclosureButton, DisclosurePanel, Menu, MenuButton, MenuItems } from '@headlessui/vue'
  import { Bars3Icon, BellIcon, XMarkIcon } from '@heroicons/vue/24/outline'

  
  const notifications = [
    { title: 'Novo comentário no seu post', time: 'Há 5 minutos' },
    { title: 'Atualização disponível', time: 'Hoje às 12:30' },
    { title: 'Tarefa atribuída a você', time: 'Ontem às 16:00' },
    { title: 'Pedido de amizade de João', time: 'Ontem às 10:45' },
    { title: 'Backup concluído com sucesso', time: '2 dias atrás' },
    { title: 'Mensagem de suporte técnico', time: '3 dias atrás' },
    { title: 'Nova versão lançada', time: '5 dias atrás' },
  ]
  </script>
  
  <style scoped>
  /* Scrollbar customizada opcional */
  ::-webkit-scrollbar {
    width: 6px;
  }
  ::-webkit-scrollbar-thumb {
    background-color: #d4d4d4;
    border-radius: 3px;
  }
  </style>
  