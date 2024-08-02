<template>
    <div>
      <h1>オセロゲーム</h1>
      <div v-if="board">
        <table>
          <tr v-for="(row, i) in board" :key="i">
            <td v-for="(cell, j) in row" :key="j" @click="placeStone(i, j)" :class="getClass(cell)">
              <div v-if="cell === 1" class="white"></div>
              <div v-if="cell === -1" class="black"></div>
            </td>
          </tr>
        </table>
        <div class="info">
          <p>白: {{ stoneCount.white }}</p>
          <p>黒: {{ stoneCount.black }}</p>
        </div>
      </div>
      <div v-if="message" class="message">{{ message }}</div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  
  const board = ref<number[][]>([])
  const stoneCount = ref<{ white: number, black: number }>({ white: 0, black: 0 })
  const message = ref<string>('')
  const currentPlayer = ref<number>(-1) // 初手は黒 (-1)
  
  const fetchBoard = async () => {
    const data = await $fetch('http://localhost:8000/get_board')
    board.value = data
  }
  
  const fetchStoneCount = async () => {
    const data = await $fetch('http://localhost:8000/count_stones')
    stoneCount.value = data
  }
  
  const placeStone = async (i: number, j: number) => {
    const color = currentPlayer.value
    const data = await $fetch('http://localhost:8000/update', {
      method: 'POST',
      body: JSON.stringify({ i, j, color })
    })
    message.value = data.message
    await fetchBoard()
    await fetchStoneCount()
    
    // プレイヤーを交代
    currentPlayer.value = currentPlayer.value === -1 ? 1 : -1
  }
  
  const getClass = (cell: number) => {
    if (cell === 1) return 'white-cell'
    if (cell === -1) return 'black-cell'
    return 'empty-cell'
  }
  
  onMounted(() => {
    fetchBoard()
    fetchStoneCount()
  })
  </script>
  
  <style>
  table {
    border-collapse: collapse;
  }
  
  td {
    width: 50px;
    height: 50px;
    border: 1px solid #000;
    text-align: center;
    vertical-align: middle;
  }
  
  .white {
    background-color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
  
  .black {
    background-color: black;
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
  
  .empty-cell {
    background-color: #00a000;
  }
  
  .white-cell {
    background-color: #00a000;
  }
  
  .black-cell {
    background-color: #00a000;
  }
  
  .info {
    margin-top: 20px;
  }
  
  .message {
    margin-top: 20px;
    color: red;
  }
  </style>
  