<script>import cc from 'classcat';
let className = undefined;
let bgColor = undefined;
let bgColorHover = undefined;
let color = undefined;
let colorHover = undefined;
let borderColor = undefined;
export { className as class };
</script>

<button
  type="button"
  on:click
  class={cc(['svelte-flow__controls-button', className])}
  style:--xy-controls-button-background-color-props={bgColor}
  style:--xy-controls-button-background-color-hover-props={bgColorHover}
  style:--xy-controls-button-color-props={color}
  style:--xy-controls-button-color-hover-props={colorHover}
  style:--xy-controls-button-border-color-props={borderColor}
  {...$$restProps}
>
  <slot class="button-svg" />
</button>
