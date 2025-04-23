<script setup>


</script>


<template>



<div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <div class="flex items-center justify-between flex-column flex-wrap md:flex-row space-y-4 md:space-y-0 pb-4">
        <div>
            <button id="dropdownActionButton" data-dropdown-toggle="dropdownAction" class="inline-flex items-center text-gray-900  border border-extra-soft-orange focus:outline-none hover:border-soft-orange focus:ring-2 focus:ring-soft-orange  font-medium rounded-lg text-sm px-3 py-1.5" type="button">
                <span class="sr-only">Action button</span>
                Action
                <svg class="w-2.5 h-2.5 ms-2.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
                </svg>
            </button>
            <!-- Dropdown menu -->
            <div id="dropdownAction" class="z-10 hidden bg-white divide-y divide-soft-orange rounded-lg shadow-sm w-44 ">
                <ul class="py-1 text-sm text-gray-900 " aria-labelledby="dropdownActionButton">
                    <li>
                        <a href="#" class="block px-4 py-2 hover:text-gray-500 ">Reward</a>
                    </li>
                    <li>
                        <a href="#" class="block px-4 py-2 hover:text-gray-500 ">Promote</a>
                    </li>
                    <li>
                        <a href="#" class="block px-4 py-2 hover:text-gray-500 ">Ativar Conta</a>
                    </li>
                </ul>
                <div class="py-1">
                    <a href="#" class="block px-4 py-2 text-sm text-gray-700  hover:text-gray-500 ">Inativar Conta</a>
                </div>
            </div>
        </div>
        <label for="table-search" class="sr-only">Search</label>
        <div class="relative">
            <div class="absolute inset-y-0 rtl:inset-r-0 start-0 flex items-center ps-3 pointer-events-none">
                <svg class="w-4 h-4 text-gray-900" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
                </svg>
            </div>
            <input type="text" id="table-search-users" class="block p-2 ps-10 text-sm rounded-lg w-80 bg-transparent border-extra-soft-orange hover:border-soft-orange focus:ring-soft-orange  placeholder-gray-500 text-gray-900 " placeholder="Search for users">
        </div>
    </div>
    <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
        <thead class="text-xs text-gray-900 uppercase bg-extra-soft-orange ">
            <tr>
                <th scope="col" class="p-4">
                    <div class="flex items-center">
                        <input id="checkbox-all-search" type="checkbox" class="w-4 h-4 text-soft-orange  border-gray-300 rounded-sm focus:ring-soft-orange dark:focus:ring-bsoft-orange dark:ring-offset-extra-soft-orange  focus:ring-2 ">
                        <label for="checkbox-all-search" class="sr-only">checkbox</label>
                    </div>
                </th>
                <th scope="col" class="px-6 py-3">
                    Nome
                </th>
                <th scope="col" class="px-6 py-3">
                    Cargo
                </th>
                <th scope="col" class="px-6 py-3">
                    Data de registo
                </th>
                <th scope="col" class="px-6 py-3">
                    Status
                </th>
                <th scope="col" class="px-6 py-3">
                    Ações
                </th>
            </tr>
        </thead>
        <tbody>
            <tr class="border-b border-soft-orange ">
                <td class="w-4 p-4">
                    <div class="flex items-center">
                        <input id="checkbox-table-search-1" type="checkbox" class="w-4 h-4 text-soft-orange  border-gray-300 rounded-sm focus:ring-soft-orange dark:focus:ring-bsoft-orange dark:ring-offset-extra-soft-orange  focus:ring-2">
                        <label for="checkbox-table-search-1" class="sr-only">checkbox</label>
                    </div>
                </td>
                <th scope="row" class="flex items-center px-6 py-4 text-gray-900 whitespace-nowrap dark:text-white">
                    <img class="w-10 h-10 rounded-full" src="" alt="Jese image">
                    <div class="ps-3">
                        <div class="text-base font-semibold text-gray-900">Neil Sims</div>
                        <div class="font-normal text-gray-500">neil.sims@flowbite.com</div>
                    </div>  
                </th>
                <td class="px-6 py-4 text-gray-900">
                    React Developer
                </td>
                <td class="px-6 py-4 text-gray-900">
                    12/04/2004
                </td>
                <td class="px-6 py-4">
                    <div class="flex items-center text-gray-900">
                        <div class="h-2.5 w-2.5 rounded-full bg-green-500 me-2"></div> Ativo
                    </div>
                </td>
                <td class="px-6 py-4">
                    <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">Edit user</a>
                </td>
            </tr>
            <tr class="border-b border-soft-orange">
                <td class="w-4 p-4">
                    <div class="flex items-center">
                        <input id="checkbox-table-search-2" type="checkbox" class="w-4 h-4 text-soft-orange  border-gray-300 rounded-sm focus:ring-soft-orange dark:focus:ring-bsoft-orange dark:ring-offset-extra-soft-orange  focus:ring-2">
                        <label for="checkbox-table-search-2" class="sr-only">checkbox</label>
                    </div>
                </td>
                <th scope="row" class="flex items-center px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    <img class="w-10 h-10 rounded-full" src="" alt="Jese image">
                    <div class="ps-3">
                        <div class="text-base font-semibold text-gray-900">Bonnie Green</div>
                        <div class="font-normal text-gray-500">bonnie@flowbite.com</div>
                    </div>
                </th>
                <td class="px-6 py-4 text-gray-900">
                    Designer
                </td>
                <td class="px-6 py-4 text-gray-900">
                    12/04/2004
                </td>
                <td class="px-6 py-4">
                    <div class="flex items-center text-gray-900">
                        <div class="h-2.5 w-2.5 rounded-full bg-green-500 me-2"></div> Ativo
                    </div>
                </td>
                <td class="px-6 py-4">
                    <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">Edit user</a>
                </td>
            </tr>
            <tr class="border-b border-soft-orange">
                <td class="w-4 p-4">
                    <div class="flex items-center">
                        <input id="checkbox-table-search-2" type="checkbox" class="w-4 h-4 text-soft-orange  border-gray-300 rounded-sm focus:ring-soft-orange dark:focus:ring-bsoft-orange dark:ring-offset-extra-soft-orange  focus:ring-2">
                        <label for="checkbox-table-search-2" class="sr-only">checkbox</label>
                    </div>
                </td>
                <th scope="row" class="flex items-center px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    <img class="w-10 h-10 rounded-full" src="" alt="Jese image">
                    <div class="ps-3">
                        <div class="text-base font-semibold text-gray-900">Jese Leos</div>
                        <div class="font-normal text-gray-500">jese@flowbite.com</div>
                    </div>
                </th>
                <td class="px-6 py-4 text-gray-900">
                    Vue JS Developer
                </td>
                <td class="px-6 py-4 text-gray-900">
                    12/04/2004
                </td>
                <td class="px-6 py-4">
                    <div class="flex items-center text-gray-900">
                        <div class="h-2.5 w-2.5 rounded-full bg-green-500 me-2"></div> Ativo
                    </div>
                </td>
                <td class="px-6 py-4">
                    <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">Edit user</a>
                </td>
            </tr>
            <tr class="border-b border-soft-orange">
                <td class="w-4 p-4">
                    <div class="flex items-center">
                        <input id="checkbox-table-search-2" type="checkbox" class="w-4 h-4 text-soft-orange  border-gray-300 rounded-sm focus:ring-soft-orange dark:focus:ring-bsoft-orange dark:ring-offset-extra-soft-orange  focus:ring-2">
                        <label for="checkbox-table-search-2" class="sr-only">checkbox</label>
                    </div>
                </td>
                <th scope="row" class="flex items-center px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    <img class="w-10 h-10 rounded-full" src="" alt="Jese image">
                    <div class="ps-3">
                        <div class="text-base font-semibold text-gray-900">Thomas Lean</div>
                        <div class="font-normal text-gray-500">thomes@flowbite.com</div>
                    </div>
                </th>
                <td class="px-6 py-4 text-gray-900">
                    UI/UX Engineer
                </td>
                <td class="px-6 py-4 text-gray-900">
                    12/04/2004
                </td>
                <td class="px-6 py-4">
                    <div class="flex items-center text-gray-900">
                        <div class="h-2.5 w-2.5 rounded-full bg-green-500 me-2"></div> Ativo
                    </div>
                </td>
                <td class="px-6 py-4">
                    <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">Edit user</a>
                </td>
            </tr>
            <tr class="border-b border-soft-orange">
                <td class="w-4 p-4">
                    <div class="flex items-center">
                        <input id="checkbox-table-search-3" type="checkbox" class="w-4 h-4 text-soft-orange  border-gray-300 rounded-sm focus:ring-soft-orange dark:focus:ring-bsoft-orange dark:ring-offset-extra-soft-orange  focus:ring-2">
                        <label for="checkbox-table-search-3" class="sr-only">checkbox</label>
                    </div>
                </td>
                <th scope="row" class="flex items-center px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    <img class="w-10 h-10 rounded-full" src="" alt="Jese image">
                    <div class="ps-3">
                        <div class="text-base font-semibold text-gray-900">Leslie Livingston</div>
                        <div class="font-normal text-gray-500">leslie@flowbite.com</div>
                    </div>
                </th>
                <td class="px-6 py-4 text-gray-900">
                    SEO Specialist
                </td>
                <td class="px-6 py-4 text-gray-900">
                    12/04/2004
                </td>
                <td class="px-6 py-4">
                    <div class="flex items-center text-gray-900">
                        <div class="h-2.5 w-2.5 rounded-full bg-red-500 me-2"></div> Inativo
                    </div>
                </td>
                <td class="px-6 py-4">
                    <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">Edit user</a>
                </td>
            </tr>
        </tbody>
    </table>
</div>


</template>