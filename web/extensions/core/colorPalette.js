import { app } from "/scripts/app.js";
import { $el } from "/scripts/ui.js";
import { api } from "/scripts/api.js";

// Manage color palettes

const colorPalettes = {
	"palette_1": {
		"id": "palette_1",
		"name": "Palette 1",
		"colors": {
			"node_slot": {
				"CLIP": "#FFD500", 
				"CLIP_VISION": "#A8DADC", 
				"CLIP_VISION_OUTPUT": "#ad7452", 
				"CONDITIONING": "#FFA931", 
				"CONTROL_NET": "#6EE7B7", 
				"IMAGE": "#64B5F6", 
				"LATENT": "#FF9CF9", 
				"MASK": "#81C784", 
				"MODEL": "#B39DDB", 
				"STYLE_MODEL": "#C2FFAE", 
				"VAE": "#FF6E6E", 
				"STRING": "#FF6E6E", 
				"NUMBER": "#FF6E6E", 
				"BOOLEAN": "#FF6E6E", 
				"FLOAT": "#FF6E6E", 
			}
		}
	},
	"solarized": {
		"id": "solarized",
		"name": "Solarized",
		"colors": {
			"node_slot": {
				"CLIP": "#556B2F", // Dark Olive Green
				"CLIP_VISION": "#4B0082", // Indigo
				"CLIP_VISION_OUTPUT": "#006400", // Green
				"CONDITIONING": "#FF1493", // Deep Pink
				"CONTROL_NET": "#8B4513", // Saddle Brown
				"IMAGE": "#8B0000", // Dark Red
				"LATENT": "#00008B", // Dark Blue
				"MASK": "#2F4F4F", // Dark Slate Grey
				"MODEL": "#FF8C00", // Dark Orange
				"STYLE_MODEL": "#004A4A", // Sherpa Blue
				"UPSCALE_MODEL": "#4A004A", // Tyrian Purple
				"VAE": "#4F394F", // Loulou
			}
		}
	},
	"takoyaro_palette": {
		"id": "takoyaro_palette",
		"name": "Takoyaro Palette",
		"colors": {
			"node_slot": {
				"CLIP": "#E8CE23", 
				"CLIP_VISION": "#DA7822", 
				"CLIP_VISION_OUTPUT": "#B44500", 
				"CONDITIONING": "#9D5AE0", 
				"CONTROL_NET": "#20E4B0", 
				"IMAGE": "#5164DF", 
				"LATENT": "#F76397", 
				"MASK": "#ABA8E6", 
				"MODEL": "#E100FF", 
				"STYLE_MODEL": "#E0A5E3", 
				"VAE": "#5BF656", 
				"RAW_TEXT": "#987B89", 
				"NUMBER": "#408994", 
				"BOOLEAN": "#B55959", 
				"FLOAT": "#949C47", 
			}
		}
	},
};

const id = "Comfy.ColorPalette";
const idCustomColorPalettes = "Comfy.CustomColorPalettes";
const defaultColorPaletteId = "palette_1";
const els = {}
// const ctxMenu = LiteGraph.ContextMenu;
app.registerExtension({
	name: id,
	init() {
		const sortObjectKeys = (unordered) => {
			return Object.keys(unordered).sort().reduce((obj, key) => {
				obj[key] = unordered[key];
				return obj;
			}, {});
		};

		const getSlotTypes = async () => {
			var types = [];

			const defs = await api.getNodeDefs();
			for (const nodeId in defs) {
				const nodeData = defs[nodeId];

				var inputs = nodeData["input"]["required"];
				if (nodeData["input"]["optional"] != undefined){
					inputs = Object.assign({}, nodeData["input"]["required"], nodeData["input"]["optional"])
				}

				for (const inputName in inputs) {
					const inputData = inputs[inputName];
					const type = inputData[0];

					if (!Array.isArray(type)) {
						types.push(type);
					}
				}

				for (const o in nodeData["output"]) {
					const output = nodeData["output"][o];
					types.push(output);
				}
			}

			return types;
		};

		const completeColorPalette = async (colorPalette) => {
			var types = await getSlotTypes();

			for (const type of types) {
				if (!colorPalette.colors.node_slot[type]) {
					colorPalette.colors.node_slot[type] = "";
				}
			}

			colorPalette.colors.node_slot = sortObjectKeys(colorPalette.colors.node_slot);

			return colorPalette;
		};

		const getColorPaletteTemplate = async () => {
			let colorPalette = {
				"id": "my_color_palette_unique_id",
				"name": "My Color Palette",
				"colors": {
					"node_slot": {
					}
				}
			};

			return completeColorPalette(colorPalette);
		};

		const getCustomColorPalettes = () => {
			return app.ui.settings.getSettingValue(idCustomColorPalettes, {});
		};

		const setCustomColorPalettes = (customColorPalettes) => {
			return app.ui.settings.setSettingValue(idCustomColorPalettes, customColorPalettes);
		};

		const addCustomColorPalette = async (colorPalette) => {
			if (typeof(colorPalette) !== "object") {
				app.ui.dialog.show("Invalid color palette");
				return;
			}

			if (!colorPalette.id) {
				app.ui.dialog.show("Color palette missing id");
				return;
			}

			if (!colorPalette.name) {
				app.ui.dialog.show("Color palette missing name");
				return;
			}

			if (!colorPalette.colors) {
				app.ui.dialog.show("Color palette missing colors");
				return;
			}

			if (colorPalette.colors.node_slot && typeof(colorPalette.colors.node_slot) !== "object") {
				app.ui.dialog.show("Invalid color palette colors.node_slot");
				return;
			}

			let customColorPalettes = getCustomColorPalettes();
			customColorPalettes[colorPalette.id] = colorPalette;
			setCustomColorPalettes(customColorPalettes);

			for (const option of els.select.childNodes) {
				if (option.value === "custom_" + colorPalette.id) {
					els.select.removeChild(option);
				}
			}

			els.select.append($el("option", { textContent: colorPalette.name + " (custom)", value: "custom_" + colorPalette.id, selected: true }));

			setColorPalette("custom_" + colorPalette.id);
			await loadColorPalette(colorPalette);
		};

		const deleteCustomColorPalette = async (colorPaletteId) => {
			let customColorPalettes = getCustomColorPalettes();
			delete customColorPalettes[colorPaletteId];
			setCustomColorPalettes(customColorPalettes);

			for (const option of els.select.childNodes) {
				if (option.value === defaultColorPaletteId) {
					option.selected = true;
				}

				if (option.value === "custom_" + colorPaletteId) {
					els.select.removeChild(option);
				}
			}

			setColorPalette(defaultColorPaletteId);
			await loadColorPalette(getColorPalette());
		};

		const loadColorPalette = async (colorPalette) => {
			colorPalette = await completeColorPalette(colorPalette);
			if (colorPalette.colors) {
				if (colorPalette.colors.node_slot) {
					Object.assign(app.canvas.default_connection_color_byType, colorPalette.colors.node_slot);
					Object.assign(LGraphCanvas.link_type_colors, colorPalette.colors.node_slot);
				}
				if (colorPalette.colors.litegraph_base) {
					// Everything updates correctly in the loop, except the Node Title and Link Color for some reason
					app.canvas.node_title_color = colorPalette.colors.litegraph_base.NODE_TITLE_COLOR;
					app.canvas.default_link_color = colorPalette.colors.litegraph_base.LINK_COLOR;

					for (const key in colorPalette.colors.litegraph_base) {
						if (colorPalette.colors.litegraph_base.hasOwnProperty(key) && LiteGraph.hasOwnProperty(key)) {
							LiteGraph[key] = colorPalette.colors.litegraph_base[key];
						}
					}
				}
				app.canvas.draw(true, true);
			}
		};

		const getColorPalette = (colorPaletteId) => {
			if (!colorPaletteId) {
				colorPaletteId = app.ui.settings.getSettingValue(id, defaultColorPaletteId);
			}

			if (colorPaletteId.startsWith("custom_")) {
				colorPaletteId = colorPaletteId.substr(7);
				let customColorPalettes = getCustomColorPalettes();
				if (customColorPalettes[colorPaletteId]) {
					return customColorPalettes[colorPaletteId];
				}
			}

			return colorPalettes[colorPaletteId];
		};

		const setColorPalette = (colorPaletteId) => {
			app.ui.settings.setSettingValue(id, colorPaletteId);
		};

		const fileInput = $el("input", {
			type: "file",
			accept: ".json",
			style: { display: "none" },
			parent: document.body,
			onchange: () => {
				let file = fileInput.files[0];

				if (file.type === "application/json" || file.name.endsWith(".json")) {
					const reader = new FileReader();
					reader.onload = async () => {
						await addCustomColorPalette(JSON.parse(reader.result));
					};
					reader.readAsText(file);
				}
			},
		});

		app.ui.settings.addSetting({
			id,
			name: "Color Palette",
			type: (name, setter, value) => {
				let options = [];

				for (const c in colorPalettes) {
					const colorPalette = colorPalettes[c];
					options.push($el("option", { textContent: colorPalette.name, value: colorPalette.id, selected: colorPalette.id === value }));
				}

				let customColorPalettes = getCustomColorPalettes();
				for (const c in customColorPalettes) {
					const colorPalette = customColorPalettes[c];
					options.push($el("option", { textContent: colorPalette.name + " (custom)", value: "custom_" + colorPalette.id, selected: "custom_" + colorPalette.id === value }));
				}

				return $el("div", [
					$el("label", { textContent: name || id }, [
						els.select = $el("select", {
							onchange: (e) => {
								setter(e.target.value);
							}
						}, options)
					]),
					$el("input", {
						type: "button",
						value: "Export",
						onclick: async () => {
							const colorPaletteId = app.ui.settings.getSettingValue(id, defaultColorPaletteId);
							const colorPalette = await completeColorPalette(getColorPalette(colorPaletteId));
							const json = JSON.stringify(colorPalette, null, 2); // convert the data to a JSON string
							const blob = new Blob([json], { type: "application/json" });
							const url = URL.createObjectURL(blob);
							const a = $el("a", {
								href: url,
								download: colorPaletteId + ".json",
								style: { display: "none" },
								parent: document.body,
							});
							a.click();
							setTimeout(function () {
								a.remove();
								window.URL.revokeObjectURL(url);
							}, 0);
						},
					}),
					$el("input", {
						type: "button",
						value: "Import",
						onclick: () => {
							fileInput.click();
						}
					}),
					$el("input", {
						type: "button",
						value: "Template",
						onclick: async () => {
							const colorPalette = await getColorPaletteTemplate();
							const json = JSON.stringify(colorPalette, null, 2); // convert the data to a JSON string
							const blob = new Blob([json], { type: "application/json" });
							const url = URL.createObjectURL(blob);
							const a = $el("a", {
								href: url,
								download: "color_palette.json",
								style: { display: "none" },
								parent: document.body,
							});
							a.click();
							setTimeout(function () {
								a.remove();
								window.URL.revokeObjectURL(url);
							}, 0);
						}
					}),
					$el("input", {
						type: "button",
						value: "Delete",
						onclick: async () => {
							let colorPaletteId = app.ui.settings.getSettingValue(id, defaultColorPaletteId);

							if (colorPalettes[colorPaletteId]) {
								app.ui.dialog.show("You cannot delete built-in color palette");
								return;
							}

							if (colorPaletteId.startsWith("custom_")) {
								colorPaletteId = colorPaletteId.substr(7);
							}

							await deleteCustomColorPalette(colorPaletteId);
						}
					}),
				]);
			},
			defaultValue: defaultColorPaletteId,
			async onChange(value) {
				if (!value) {
					return;
				}

				if (colorPalettes[value]) {
					await loadColorPalette(colorPalettes[value]);
				} else if (value.startsWith("custom_")) {
					value = value.substr(7);
					let customColorPalettes = getCustomColorPalettes();
					if (customColorPalettes[value]) {
						await loadColorPalette(customColorPalettes[value]);
					}
				}
			},
		});
	},
});
