import { app } from "../../../scripts/app.js"

const TypeSlot = {
    Input: 1,
    Output: 2,
};

const TypeSlotEvent = {
    Connect: true,
    Disconnect: false,
};

const _ID = "CustomCodeNode";
const _PREFIX = "any";
const _TYPE = "IMAGE";

app.registerExtension({
	name: 'CustomCodeNode.' + _ID,
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // skip the node if it is not the one we want
        if (nodeData.name !== _ID) {
            return
        }

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = async function () {
            onNodeCreated?.apply(this);
            this.builtinNum = this.inputs.length;
            this.outputs = [];
            this.addInput("var0", "*");
            this.addOutput("var0", "*");
            this._size[1] = 400;
            this?.graph?.setDirtyCanvas(true);
        }

        const onConnectionsChange = nodeType.prototype.onConnectionsChange
        nodeType.prototype.onConnectionsChange = function (slotType, slot_idx, event, link_info, node_slot) {
            const me = onConnectionsChange?.apply(this, arguments);
            
            if (slotType === TypeSlot.Input)
            {
                if (slot_idx >= this.builtinNum)
                {
                    const varidx = slot_idx - this.builtinNum;
                    if (link_info && event === TypeSlotEvent.Connect) {
                        // get the parent (left side node) from the link
                        const fromNode = this.graph._nodes.find(
                            (otherNode) => otherNode.id == link_info.origin_id
                        )
    
                        if (varidx == this.inputs.length - this.builtinNum - 1)
                        {
                            this.addInput("var" + (varidx + 1), "*");
                            this.addOutput("var" + (varidx + 1), "*");
                        }
                    }
                    else if (event === TypeSlotEvent.Disconnect) {

                        let idx = this.inputs.length - 1;
                        while(idx > this.builtinNum)
                        {
                            let front = idx - 1;
                            let front_linked = this.inputs[front].link != null;
                            
                            if (this.inputs[idx].link == null && !front_linked)
                            {
                                this.removeInput(idx);
                                this.removeOutput(idx - this.builtinNum);
                            }
                            else
                            {
                                break;
                            }
                            idx--;
                        }
                    }
    
                    this?.graph?.setDirtyCanvas(true);
                    return me;
                }
            }
        }
        return nodeType;
    },

})