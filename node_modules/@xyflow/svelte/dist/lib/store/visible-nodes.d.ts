/// <reference types="svelte" />
/// <reference types=".pnpm/svelte@4.2.1/node_modules/svelte" />
import type { SvelteFlowStoreState } from './types';
export declare function getVisibleNodes(store: SvelteFlowStoreState): import("svelte/store").Readable<import("..").InternalNode[]>;
