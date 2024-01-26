<template>
  <Header />
  <LoadingSpinner :isLoading="isLoading" />

  <section>
    <div>
      <div class="center">
        <div class="title">
          <h1 v-if="!file">Drop file to upload</h1>
          <h1 v-if="file">{{ file.name }}</h1>
          <div class="selection-bar-div">
           <select class="selection-bar" v-model="mode">
            <option value="single_line">Single Line</option>
            <option value="whole sheet">Whole Sheet</option>
        </select>
        </div>
        </div>

        <div class="dropzone">
          <img
            src="http://100dayscss.com/codepen/upload.svg"
            class="upload-icon"
          />
          <input
            type="file"
            class="upload-input"
            @change="handleFileUpload($event)"
          />
        </div>
       

        <button
          v-on:click="submitFile()"
          type="button"
          class="btn"
          name="uploadbutton"
        >
          Upload file
        </button>


      </div>
    </div>
  </section>
  <div class="performance_data">
    <h2>OMR Result：</h2>
    <div class="wrapper" v-if="result">
      <div class="result_img">
        <img src="../../Output/output_bboxes.png" alt="">
      </div>
      <div class="result_img">
        <img src="../../Output/ouptut_result.png" alt="">
      </div>
    </div>

  </div>

</template>
<script>
import Header from "./components/header.vue";
// import Table from "./components/table.vue";
import LoadingSpinner from "./components/LoadingSpinner.vue";
export default {
  name: "App",
  components: {
    Header,
    // Table,
    LoadingSpinner,
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
      console.log(event.target.files[0]);
    },
    
    
    async submitFile() {
      this.isLoading = true;
      this.result=false;

      let formData = new FormData();
      formData.append("file", this.file);
      formData.append("mode", this.mode)
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",

        body: formData,
      });
      console.log("response:", response);
      this.result = true
      // this.performance = await response.json();
      this.isLoading = false;
    },
  },
  data() {
    return {
      file: "",
      isLoading: false,
      result: false,
      mode: "",
    };
  },
};
</script>

<style>

img {
  width: 100%;
}

.result_img {
  width: 500px;
}


#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.header {
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: var(--z-fixed);
  background-color: rgb(76, 140, 224);
}

.center {
  position: fixed;
  top: 20%;
  left: 15%;
  width: 300px;
  height: 260px;
  border-radius: 2rem;
  box-shadow: 8px 10px 15px 0 rgba(0, 0, 0, 0.2);
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  flex-direction: column;
}




.title {
  width: 100%;
  height: 50px;
  border-bottom: 1px solid #999;
  text-align: center;
}

h1 {
  font-size: 16px;
  font-weight: 300;
  color: #666;
}

.dropzone {
  width: 100px;
  height: 80px;
  border: 1px dashed #999;
  border-radius: 3px;
  text-align: center;
}

.upload-icon {
  margin: 25px 2px 2px 2px;
}

.upload-input {
  position: relative;
  top: -62px;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
}

.btn {
  display: block;
  width: 140px;
  height: 40px;
  background: rgb(76, 140, 224);
  color: #fff;
  border-radius: 3px;
  border: 0;
  box-shadow: 0 3px 0 0 rgb(4, 98, 153);
  transition: all 0.3s ease-in-out;
  font-size: 14px;
}

.btn:hover {
  background: rgb(4, 98, 153);
  box-shadow: 0 3px 0 0 white;
}

.performance_data {
  position: fixed;
  top: 20%;
  right: 50px;

  width: 50%;
}
.performance_data h2 {
  float: left;
  margin-left: 3rem;
}
.performance_data .wrapper {
  display: flex;
  padding: 2rem;
  overflow-x: scroll;
  width: 100%;
}
.round_button {
  border-radius: 10px;
  border-color: white;
  background:rgb(76, 140, 224);
  color: white;
  padding: 15px 20px;
  cursor: pointer;
  transition: 1s;
}

.round_button:hover {
  background: rgb(4, 98, 153);
  box-shadow: 0 3px 0 0 white;
}

.performance_data .round_button {
  float: left;
  margin-left: 5rem;
}

.graph {
  position: fixed;
  left: 10%;
  top: 35%;
  width: 450px;
  z-index: -1;
}
.graph img {
  width: 100%;
}



</style>
