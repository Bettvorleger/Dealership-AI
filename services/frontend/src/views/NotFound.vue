<template>
  <main class="container">
    <div class="container__left venn" role="img" aria-label="404 Venn Diagram">
      <div class="venn__bubble venn__bubble--left" aria-hidden="true"></div>
      <div class="venn__bubble venn__bubble--right" aria-hidden="true"></div>
      <p class="venn__text venn__text--left" aria-describedby="venn-left">
        We broke Something
      </p>
      <p class="venn__text venn__text--center" aria-describedby="venn-center">
        404
      </p>
      <p class="venn__text venn__text--right" aria-describedby="venn-right">
        You cannot type
      </p>
      <span id="venn-left" class="sr-only">Left side of venn diagram</span>
      <span id="venn-center" class="sr-only"
        >Intersect side of venn diagram</span
      >
      <span id="venn-right" class="sr-only">Right side of venn diagram</span>
    </div>
    <div class="container__right desc">
      <h6 class="desc__head">Error: 404 - Page Not Found</h6>
      <div class="desc__body">
        <p>You might be here because:</p>
        <ul>
          <li>The page has moved</li>
          <li>The page no longer exists</li>
          <li>You were looking for your kittens and got lost</li>
          <li>You like 404 pages</li>
        </ul>
      </div>
    </div>
  </main>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>

@import '@/styles/404vars.css';

.sr-only {
  position: absolute;
  width: 0.0625rem;
  height: 0.0625rem;
  margin: -0.0625rem;
  padding: 0;
  clip: rect(0.0625rem, 0.0625rem, 0.0625rem, 0.0625rem);
  -webkit-clip-path: inset(50%);
  clip-path: inset(50%);
  overflow: hidden;
}

.container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100%;
}
.container__left {
  margin-top: 1rem;
}
.venn {
  display: grid;
  grid-template-columns: repeat(3, var(--venn-base-size));
  grid-template-areas: "left center right";
}
.venn__bubble {
  grid-row: 1;
  display: flex;
  align-items: center;
  height: calc(var(--venn-base-size) * 2);
  border-radius: 12.5rem;
}
.venn__bubble--left {
  grid-column-start: left;
  grid-column-end: center;
  background-color: var(--secondary);
  border: 2px solid rgba(0, 0, 0, 0.2);
  box-shadow: inset var(--venn-base-size) 0 var(--secondary);
}
.venn__bubble--right {
  grid-column-start: center;
  grid-column-end: right;
  justify-content: flex-end;
  background: var(--tertiary)
    repeating-linear-gradient(
      45deg,
      rgba(0, 0, 0, 0.2) 0rem,
      rgba(0, 0, 0, 0) 0.0625rem,
      rgba(0, 0, 0, 0) 0.5rem,
      rgba(0, 0, 0, 0.2) 0.5625rem
    );
  border: 2px solid rgba(0, 0, 0, 0.2);
  box-shadow: inset calc(var(--venn-base-size) * -1) 0 var(--tertiary);
  mix-blend-mode: hard-light;
}
.venn__text {
  position: relative;
  grid-row: 1;
  display: flex;
  align-items: center;
  padding: 1rem;
  height: calc(var(--venn-base-size) * 2);
  font-size: 1.5rem;
  line-height: 1.5;
  font-weight: normal;
  z-index: 1;
}
.venn__text--left {
  grid-column-start: left;
  grid-column-end: left;
  justify-content: flex-start;
  color: var(--primary-text-on-secondary);
}
.venn__text--center {
  grid-column-start: center;
  grid-column-end: center;
  justify-content: center;
  font-size: 3rem;
  color: var(--primary-text-on-primary);
}
.venn__text--right {
  grid-column-start: right;
  grid-column-end: right;
  justify-content: flex-end;
  text-align: right;
  color: var(--primary-text-on-tertiary);
}

.desc {
  width: 100%;
  max-width: calc(var(--venn-base-size) * 2);
}
.desc__head {
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
  text-align: center;
  border-bottom: var(--border-on-light);
}
.desc__body {
  color: var(--disabled-text-on-light);
}

@media (max-width: 43.75rem) {
  .venn__text {
    font-size: 0.875rem;
    font-weight: normal;
  }

  .desc {
    max-width: calc(var(--venn-base-size) * 3);
  }
}
</style>
