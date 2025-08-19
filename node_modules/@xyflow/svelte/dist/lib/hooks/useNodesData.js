import { derived } from 'svelte/store';
import { shallowNodeData } from '@xyflow/system';
import { useStore } from '../store';
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function useNodesData(nodeIds) {
    const { nodes, nodeLookup } = useStore();
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    let prevNodesData = [];
    return derived([nodes, nodeLookup], ([, nodeLookup], set) => {
        const nextNodesData = [];
        const isArrayOfIds = Array.isArray(nodeIds);
        const _nodeIds = isArrayOfIds ? nodeIds : [nodeIds];
        for (const nodeId of _nodeIds) {
            const node = nodeLookup.get(nodeId)?.internals.userNode;
            if (node) {
                nextNodesData.push({
                    id: node.id,
                    type: node.type,
                    data: node.data
                });
            }
        }
        if (!shallowNodeData(nextNodesData, prevNodesData)) {
            prevNodesData = nextNodesData;
            set(isArrayOfIds ? nextNodesData : nextNodesData[0] ?? null);
        }
    });
}
