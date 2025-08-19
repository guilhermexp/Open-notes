<script lang="ts">
	import { onMount } from 'svelte';
	import YouTubePlayer from '../common/YouTubePlayer.svelte';
	
	export let container: HTMLElement;
	
	let youtubePreviews: Map<string, boolean> = new Map();
	
	function extractYouTubeId(url: string): string | null {
		const patterns = [
			/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/)([^&\n?#]+)/,
			/youtube\.com\/watch\?.*v=([^&\n?#]+)/
		];
		
		for (const pattern of patterns) {
			const match = url.match(pattern);
			if (match && match[1]) {
				return match[1];
			}
		}
		return null;
	}
	
	function processYouTubeLinks() {
		if (!container) return;
		
		// Find all links in the container
		const links = container.querySelectorAll('a[href*="youtube.com"], a[href*="youtu.be"]');
		
		links.forEach((link: HTMLAnchorElement) => {
			const videoId = extractYouTubeId(link.href);
			if (!videoId) return;
			
			// Check if this link already has a preview button
			if (link.nextElementSibling?.classList.contains('youtube-preview-toggle')) {
				return;
			}
			
			// Create the eye button
			const eyeButton = document.createElement('button');
			eyeButton.className = 'youtube-preview-toggle inline-flex items-center justify-center ml-1 p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors';
			eyeButton.innerHTML = `
				<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
					<path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
					<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
				</svg>
			`;
			eyeButton.title = 'Show/Hide YouTube Preview';
			
			// Create preview container
			const previewContainer = document.createElement('div');
			previewContainer.className = 'youtube-preview-container hidden mt-2';
			previewContainer.dataset.videoId = videoId;
			
			// Insert button and container after the link
			link.parentNode?.insertBefore(eyeButton, link.nextSibling);
			eyeButton.parentNode?.insertBefore(previewContainer, eyeButton.nextSibling);
			
			// Add click handler to toggle preview
			eyeButton.addEventListener('click', (e) => {
				e.preventDefault();
				e.stopPropagation();
				togglePreview(videoId, previewContainer);
			});
		});
	}
	
	function togglePreview(videoId: string, container: HTMLElement) {
		const isVisible = !container.classList.contains('hidden');
		
		if (isVisible) {
			// Hide preview
			container.classList.add('hidden');
			container.innerHTML = '';
			youtubePreviews.set(videoId, false);
		} else {
			// Show preview
			container.classList.remove('hidden');
			container.innerHTML = `
				<div class="youtube-player-wrapper my-2">
					<div class="relative w-full" style="padding-bottom: 56.25%;">
						<iframe
							class="absolute top-0 left-0 w-full h-full rounded-lg"
							src="https://www.youtube.com/embed/${videoId}"
							title="YouTube video player"
							frameborder="0"
							allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
							allowfullscreen
						></iframe>
					</div>
				</div>
			`;
			youtubePreviews.set(videoId, true);
		}
	}
	
	onMount(() => {
		// Process links when component mounts
		processYouTubeLinks();
		
		// Watch for changes in the container
		const observer = new MutationObserver(() => {
			processYouTubeLinks();
		});
		
		if (container) {
			observer.observe(container, {
				childList: true,
				subtree: true
			});
		}
		
		return () => {
			observer.disconnect();
		};
	});
</script>

<style>
	:global(.youtube-preview-toggle) {
		display: inline-flex !important;
		vertical-align: middle;
		margin-left: 0.25rem;
	}
	
	:global(.youtube-preview-container) {
		margin-top: 0.5rem;
		margin-bottom: 0.5rem;
	}
	
	:global(.youtube-player-wrapper) {
		max-width: 640px;
	}
</style>