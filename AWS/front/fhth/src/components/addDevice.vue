<template>
    <div id="addDevice">
        <el-input id= "a" placeholder="시리얼 코드" v-model="data.serial" class="input-with-select" @change="validationCheck">
            <el-select v-model="data.type" slot="prepend" placeholder="디바이스" style="width:200px;" @change="validationCheck">
                <el-option v-for="device in deviceList" v-bind:key= "device.id" :value="device.type">{{device.type}}</el-option>
            </el-select>
        </el-input>
  </div>
</template>

<script>
import {deviceAPI} from "../utils/axios"
export default {
    props:['deviceList', "data"],
    data() {
        return {
            colors : "primary",
            form : {
                type: "",
                serial : ""
            },
        }
    },
    methods: {
        async validationCheck() {
            const {result} = (await deviceAPI.verifyRegistedDevice(this.data)).data
            console.log({id:this.data.id, validation:result})
            this.$emit("update",{id:this.data.id, validation:result})
        }
    }
}
</script>

<style>
  .el-select .el-input {
    width: 110px;
  }
</style>