<script lang="ts">
	export let videoId: string;
	export let title: string = '';
	export let width: number = 560;
	export let height: number = 315;
	export let autoplay: boolean = false;
	export let muted: boolean = false;
	export let controls: boolean = true;
	export let loop: boolean = false;
	export let start: number = 0;
	
	$: embedUrl = `https://www.youtube-nocookie.com/embed/${videoId}?${new URLSearchParams({
		autoplay: autoplay ? '1' : '0',
		mute: muted ? '1' : '0',
		controls: controls ? '1' : '0',
		loop: loop ? '1' : '0',
		start: start.toString(),
		rel: '0',
		modestbranding: '1'
	}).toString()}`;
</script>

<div class="youtube-player-container w-full">
	<div class="relative pb-[56.25%] h-0 overflow-hidden rounded-lg shadow-lg">
		<iframe
			{title}
			src={embedUrl}
			frameborder="0"
			allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
			allowfullscreen
			class="absolute top-0 left-0 w-full h-full"
		/>
	</div>
</div>

<style>
	.youtube-player-container {
		max-width: 100%;
	}
</style>