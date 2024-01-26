<template>
    <div v-if="isLoading" class="loading">
      <pulse-loader
        color="#343A4B"
        size="1.5rem"
        class="loadingSpinner"
      ></pulse-loader>
    </div>
</template>

<script>
export default {
    props: {
        isLoading: {
            type: Boolean,
            default: false,
        }
    }
}
</script>

<style scoped>
.loading {
  position: fixed;
  height: 100vh;
  width: 100%;
  z-index: 1;
  background: linear-gradient(
    rgba(255, 255, 255, 0.678),
    rgba(255, 255, 255, 0.199)
  );
}

.loadingSpinner {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>