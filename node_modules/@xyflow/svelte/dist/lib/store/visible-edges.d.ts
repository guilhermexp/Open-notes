/// <reference types="svelte" />
/// <reference types=".pnpm/svelte@4.2.1/node_modules/svelte" />
import type { EdgeLayouted } from '../types';
import type { SvelteFlowStoreState } from './types';
export declare function getVisibleEdges(store: SvelteFlowStoreState): import("svelte/store").Readable<EdgeLayouted[]>;
