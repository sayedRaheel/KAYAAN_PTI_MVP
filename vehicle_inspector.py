# %% Import required libraries
import streamlit as st
import base64
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
# %% Initialize OpenAI Client

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# %% Component Prompt Registry (truncated for brevity - use your full registry)

# %% Component Prompt Registry
PROMPT_REGISTRY = {
    "truck_steering_tires": {
        "system_prompt": """Analyze steering tire image for safety and compliance:
1. Tread depth measurement (minimum 4/32")
2. Sidewall condition (no cuts, bulges, damage)
3. Inflation status (visual assessment)
4. Mounting security (all lug nuts present and tight)
5. Rim condition (no cracks or damage)
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "tread_depth_32nds": number,
    "pressure_status": "normal|low|high",
    "wear_type": "even|inner|outer|irregular",
    "sidewall_condition": "good|damaged",
    "lug_nut_status": "complete|missing",
    "rim_integrity": "good|damaged",
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "truck_rear_tires": {
        "system_prompt": """Analyze rear tire set for safety and compliance:
1. Inter-tire clearance (minimum 1 inch)
2. Matching tread patterns
3. Debris between tires
4. Inflation consistency
5. Tread depth (minimum 2/32")
6. Dual tire matching
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "clearance_inches": number,
    "debris_present": boolean,
    "inflation_match": boolean,
    "tread_depth_32nds": number,
    "tire_matching": "matched|mismatched",
    "wear_pattern": "even|uneven",
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "truck_mirrors": {
        "system_prompt": """Analyze truck mirrors for safety and compliance:
1. Mount security
2. Surface integrity
3. Proper positioning
4. Coverage angle
5. Hood/fender mirror condition
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "mount_secure": boolean,
    "surface_condition": "clear|damaged",
    "position_correct": boolean,
    "coverage_adequate": boolean,
    "fender_mirror_status": "intact|damaged|missing",
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "truck_bumper": {
        "system_prompt": """Analyze truck bumper for safety and compliance:
1. Mount security
2. Height alignment
3. Structural integrity
4. No sagging
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "mount_secure": boolean,
    "height_correct": boolean,
    "structural_integrity": "good|compromised",
    "sagging_present": boolean,
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "truck_lights": {
        "system_prompt": """Analyze truck head lighting for safety and compliance:
1. All lights ON in image
2. Proper color (amber/red)
3. Lens condition
4. Even brightness
5. Proper mounting
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "lights_functional": boolean,
    "color_correct": boolean,
    "lens_condition": "clear|damaged",
    "brightness_even": boolean,
    "mount_secure": boolean,
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "mud_flaps": {
        "system_prompt": """Analyze mud flaps for safety and compliance:
1. Proper height from ground
2. Secure mounting
3. No damage/tears
4. Width coverage
5. Anti-spray compliance
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "height_correct": boolean,
    "mount_secure": boolean,
    "condition": "good|damaged",
    "width_adequate": boolean,
    "spray_compliant": boolean,
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "windshield_wipers": {
        "system_prompt": """Analyze windshield and wipers for safety:
1. Windshield integrity
2. Wiper blade condition
3. Wiper arm function
4. Proper coverage
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "windshield_condition": "clear|damaged",
    "blade_condition": "good|worn|damaged",
    "arm_function": "normal|impaired",
    "coverage_complete": boolean,
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "under_hood_fluid_inspection": {
        "system_prompt": """Analyze under hood fluid levels - MUST see actual fluid line, not just container:
1. Check fluid line against MIN/MAX marks
2. Verify fluid is visible (not just empty container)
3. Check for leaks/stains
4. Verify normal fluid colors
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "washer_fluid": {
        "level": "full|low|empty",
        "fluid_visible": boolean
    },
    "coolant": {
        "level": "full|low|empty",
        "fluid_visible": boolean
    },
    "oil": {
        "level": "full|low|empty",
        "fluid_visible": boolean
    },
    "leaks_detected": boolean,
    "colors_normal": boolean,
    "remark": string
}"""
    },

    "trailer_inspection": {
        "system_prompt": """Analyze trailer condition and compliance:
1. Body panel condition
2. Reflective tape status
3. Door seals/operation
4. Landing gear condition
5. Coupling security
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "body_condition": "good|damaged",
    "reflective_tape": "complete|incomplete",
    "door_seals": "good|damaged",
    "landing_gear": "functional|damaged",
    "coupling_secure": boolean,
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "trailer_tires": {
        "system_prompt": """Analyze trailer tires for safety:
1. Tread depth (minimum 2/32")
2. Matching pairs
3. Proper spacing
4. Inflation status
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "tread_depth_32nds": number,
    "pairs_matched": boolean,
    "spacing_adequate": boolean,
    "inflation_status": "normal|low|high",
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "trailer_lights": {
        "system_prompt": """Analyze trailer lighting systems:
1. Brake lights function
2. Turn signals
3. Marker lights
4. Reflector condition
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "brake_lights": "functional|failed",
    "turn_signals": "functional|failed",
    "markers": "complete|incomplete",
    "reflectors": "good|damaged",
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    }
}
# %% Image Encoding Function
def encode_image(image_data):
    return base64.b64encode(image_data).decode('utf-8')

# %% Analysis Function
def analyze_vehicle_component(component_type, image_data):
    if component_type not in PROMPT_REGISTRY:
        return {"error": f"Unsupported component type: {component_type}"}
    
    try:
        base64_image = encode_image(image_data)
        messages = [
            {
                "role": "system",
                "content": PROMPT_REGISTRY[component_type]["system_prompt"]
            },
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}", "detail": "high"}},
                    {"type": "text", "text": "Analyze this image and provide the required JSON output."}
                ]
            }
        ]
        
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=0.0,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        result["component_type"] = component_type
        return result
        
    except Exception as e:
        return {"error": str(e)}

# %% Streamlit UI
st.set_page_config(page_title="Vehicle Inspector", layout="wide")
st.title("🚛 KAYAAN: Vehicle Component Safety Inspector")
st.write("Upload an image and select component type for safety analysis")

# Component selection
component_type = st.selectbox(
    "Select Component Type",
    options=list(PROMPT_REGISTRY.keys()),
    index=0
)

# Image upload
uploaded_file = st.file_uploader(
    "Upload Vehicle Component Image",
    type=["jpg", "jpeg", "png"],
    help="Upload clear image of the vehicle component for analysis"
)

# Analysis button
if st.button("Analyze Component"):
    if not uploaded_file:
        st.warning("Please upload an image first")
        st.stop()
    
    with st.spinner("Analyzing component..."):
        try:
            image_data = uploaded_file.read()
            result = analyze_vehicle_component(component_type, image_data)
            
            if "error" in result:
                st.error(f"Analysis failed: {result['error']}")
            else:
                st.subheader("Analysis Results")
                st.json(result)
                
                if result.get("status") == "pass":
                    st.success("✅ Component meets safety standards")
                else:
                    st.error("❌ Component requires attention")
                
        except Exception as e:
            st.error(f"Analysis error: {str(e)}")
