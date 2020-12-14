// construct an adjacency list to replicate the pipeline graph
let adjacencyList = {}

function addVertex(vertex) {
  if (!adjacencyList[vertex]) {
    adjacencyList[vertex] = []
  }
}

function addEdge(source, destination) {
  if (!adjacencyList[source]) {
    addVertex(source)
  }
  if (!adjacencyList[destination]) {
    addVertex(destination)
  }
  adjacencyList[source].push(destination)
  adjacencyList[destination].push(source)
}

// DFS
function depthFirstSearch(startingVertex, sceneNodes) {
  const result = []
  const stack = [startingVertex]
  const visited = {}
  visited[startingVertex] = true
  let currentVertex
  while (stack.length) {
    currentVertex = stack.pop()
    result.push(currentVertex)
    adjacencyList[currentVertex]?.forEach(neighbour => {
      if (!visited[neighbour]) {
        visited[neighbour] = true
        stack.push(neighbour)
      }
    })
  }

  // DFS result must match pipeline nodes length to be connected
  return sceneNodes.length === result.length
}

export function pipelineValidator(nodes, links) {
  adjacencyList = {}

  // inital nodes in graph to compare with result nodes after DFS
  const sceneNodes = nodes.map(node => {
    return node.id
  })
  // populate adjaceny list
  nodes.forEach(node => {
    addVertex(node.id)
  })
  links.forEach(link => {
    addEdge(link.from, link.to)
  })
  // use first key(vertex) in adjacency list as the starting vertex for DFS
  return depthFirstSearch(Object.keys(adjacencyList)[0], sceneNodes)
}
