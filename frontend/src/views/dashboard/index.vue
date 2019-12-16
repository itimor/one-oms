<template>
  <el-row class="dashboard-editor-container">
    <panel-group @handleSetLineChartData="handleSetLineChartData"/>
    <el-row class="home-middle" :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 12}" :md="{span: 12}" :lg="{span: 6}" :xl="{span: 6}">
        <box-card/>
      </el-col>
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 12}" :xl="{span: 12}">
        <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 12}" :xl="{span: 8}">
          <pan-thumb :image="avatar" style="float: left">
            <span class="pan-info-roles">{{ username }}</span>
          </pan-thumb>
        </el-col>
        <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 12}" :xl="{span: 16}">
          <div class="info-container">
            <el-row>
              <span class="display_name">Hi！{{ username }}</span>
              <span class="introduction">{{ introduction }}</span>
              <img :src="emptyGif" class="emptyGif">
            </el-row>
          </div>
        </el-col>
      </el-col>
      <el-col :xs="{span: 24}" :sm="{span: 12}" :md="{span: 12}" :lg="{span: 6}" :xl="{span: 6}">
        <todo-list/>
      </el-col>
    </el-row>
    
    <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <raddar-chart/>
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <pie-chart/>
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <bar-chart/>
        </div>
      </el-col>
    </el-row>
  </el-row>
</template>

<script>
  import PanelGroup from './components/PanelGroup'
  import RaddarChart from './components/RaddarChart'
  import PieChart from './components/PieChart'
  import BarChart from './components/BarChart'
  import TodoList from './components/TodoList'
  import BoxCard from './components/BoxCard'
  import PanThumb from '@/components/PanThumb'
  import {mapGetters} from 'vuex'
  
  const lineChartData = {
    newVisitis: {
      expectedData: [100, 120, 161, 134, 105, 160, 165],
      actualData: [120, 82, 91, 154, 162, 140, 145]
    },
    messages: {
      expectedData: [200, 192, 120, 144, 160, 130, 140],
      actualData: [180, 160, 151, 106, 145, 150, 130]
    },
    purchases: {
      expectedData: [80, 100, 121, 104, 105, 90, 100],
      actualData: [120, 90, 100, 138, 142, 130, 130]
    },
    shoppings: {
      expectedData: [130, 140, 141, 142, 145, 150, 160],
      actualData: [120, 82, 91, 154, 162, 140, 130]
    }
  }
  
  export default {
    name: 'DashboardAdmin',
    components: {
      PanelGroup,
      RaddarChart,
      PieChart,
      BarChart,
      TodoList,
      BoxCard,
      PanThumb
    },
    data() {
      return {
        lineChartData: lineChartData.newVisitis,
        emptyGif: 'https://wpimg.wallstcn.com/0e03b7da-db9e-4819-ba10-9016ddfdaed3' // '/resource/img/walk.gif'
      }
    },
    computed: {
      ...mapGetters([
        'username',
        'avatar',
        'introduction',
      ])
    },
    methods: {
      handleSetLineChartData(type) {
        this.lineChartData = lineChartData[type]
      }
    }
  }
</script>

<style lang="scss" scoped>
  .dashboard-editor-container {
    padding: 32px;
    background-color: rgb(240, 242, 245);
    position: relative;
    
    .home-middle {
      margin-bottom: 20px;
      .info-container {
        line-height: 200px;
        .display_name {
          font-size: 32px;
          line-height: 48px;
          color: #40c9c6;
          position: absolute;
        }
        .introduction {
          font-size: 24px;
          font-style: italic;
          line-height: 32px;
          color: #c0c4cc;
        }
      }
      .emptyGif {
        display: block;
        width: 60%;
        margin: 0 auto;
      }
    }
    .chart-wrapper {
      background: #fff;
      padding: 16px 16px 0;
      margin-bottom: 32px;
    }
  }
</style>
