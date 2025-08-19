import { readable, writable } from 'svelte/store';
import { infiniteExtent, SelectionMode, ConnectionMode, ConnectionLineType, devWarn, adoptUserNodes, getViewportForBounds, updateConnectionLookup, initialConnection, getInternalNodesBounds } from '@xyflow/system';
import DefaultNode from '../components/nodes/DefaultNode.svelte';
import InputNode from '../components/nodes/InputNode.svelte';
import OutputNode from '../components/nodes/OutputNode.svelte';
import GroupNode from '../components/nodes/GroupNode.svelte';
import { BezierEdgeInternal, SmoothStepEdgeInternal, StraightEdgeInternal, StepEdgeInternal } from '../components/edges';
import { createNodesStore, createEdgesStore } from './utils';
export const initialNodeTypes = {
    input: InputNode,
    output: OutputNode,
    default: DefaultNode,
    group: GroupNode
};
export const initialEdgeTypes = {
    straight: StraightEdgeInternal,
    smoothstep: SmoothStepEdgeInternal,
    default: BezierEdgeInternal,
    step: StepEdgeInternal
};
export const getInitialStore = ({ nodes = [], edges = [], width, height, fitView, nodeOrigin, nodeExtent }) => {
    const nodeLookup = new Map();
    const parentLookup = new Map();
    const connectionLookup = new Map();
    const edgeLookup = new Map();
    const storeNodeOrigin = nodeOrigin ?? [0, 0];
    const storeNodeExtent = nodeExtent ?? infiniteExtent;
    adoptUserNodes(nodes, nodeLookup, parentLookup, {
        nodeExtent: storeNodeExtent,
        nodeOrigin: storeNodeOrigin,
        elevateNodesOnSelect: false,
        checkEquality: false
    });
    updateConnectionLookup(connectionLookup, edgeLookup, edges);
    let viewport = { x: 0, y: 0, zoom: 1 };
    if (fitView && width && height) {
        const bounds = getInternalNodesBounds(nodeLookup, {
            filter: (node) => !!((node.width || node.initialWidth) && (node.height || node.initialHeight))
        });
        viewport = getViewportForBounds(bounds, width, height, 0.5, 2, 0.1);
    }
    return {
        flowId: writable(null),
        nodes: createNodesStore(nodes, nodeLookup, parentLookup, storeNodeOrigin, storeNodeExtent),
        nodeLookup: readable(nodeLookup),
        parentLookup: readable(parentLookup),
        edgeLookup: readable(edgeLookup),
        visibleNodes: readable([]),
        edges: createEdgesStore(edges, connectionLookup, edgeLookup),
        visibleEdges: readable([]),
        connectionLookup: readable(connectionLookup),
        height: writable(500),
        width: writable(500),
        minZoom: writable(0.5),
        maxZoom: writable(2),
        nodeOrigin: writable(storeNodeOrigin),
        nodeDragThreshold: writable(1),
        nodeExtent: writable(storeNodeExtent),
        translateExtent: writable(infiniteExtent),
        autoPanOnNodeDrag: writable(true),
        autoPanOnConnect: writable(true),
        fitViewOnInit: writable(false),
        fitViewOnInitDone: writable(false),
        fitViewOptions: writable(undefined),
        panZoom: writable(null),
        snapGrid: writable(null),
        dragging: writable(false),
        selectionRect: writable(null),
        selectionKeyPressed: writable(false),
        multiselectionKeyPressed: writable(false),
        deleteKeyPressed: writable(false),
        panActivationKeyPressed: writable(false),
        zoomActivationKeyPressed: writable(false),
        selectionRectMode: writable(null),
        selectionMode: writable(SelectionMode.Partial),
        nodeTypes: writable(initialNodeTypes),
        edgeTypes: writable(initialEdgeTypes),
        viewport: writable(viewport),
        connectionMode: writable(ConnectionMode.Strict),
        domNode: writable(null),
        connection: readable(initialConnection),
        connectionLineType: writable(ConnectionLineType.Bezier),
        connectionRadius: writable(20),
        isValidConnection: writable(() => true),
        nodesDraggable: writable(true),
        nodesConnectable: writable(true),
        elementsSelectable: writable(true),
        selectNodesOnDrag: writable(true),
        markers: readable([]),
        defaultMarkerColor: writable('#b1b1b7'),
        lib: readable('svelte'),
        onlyRenderVisibleElements: writable(false),
        onerror: writable(devWarn),
        ondelete: writable(undefined),
        onedgecreate: writable(undefined),
        onconnect: writable(undefined),
        onconnectstart: writable(undefined),
        onconnectend: writable(undefined),
        onbeforedelete: writable(undefined),
        nodesInitialized: writable(false),
        edgesInitialized: writable(false),
        viewportInitialized: writable(false),
        initialized: readable(false)
    };
};
