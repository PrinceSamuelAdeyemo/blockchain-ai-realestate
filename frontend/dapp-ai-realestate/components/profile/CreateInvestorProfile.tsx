"use clients"

import React, {useState, useEffect, useRef} from "react"
import Modal from '@/components/Modal'


interface InvestorProfile{
        min_investment: number,
        max_investment: number,
        target_roi: number,
        preferred_hold_period: number,
        wants_dividend_reinvestment: boolean,
        investment_goals: string,
        alert_on_new_properties: BinaryType,
        preferred_property_types: Array<{
            id: string
            category: string,
            name: string
        }>
}

interface ModalProps{
    modalOpen: boolean,
    setModalOpen: React.Dispatch<React.SetStateAction<boolean>>,
    submitText?: string
}

const CreateInvestorProfile:React.FC<ModalProps> = ({modalOpen, setModalOpen, submitText}) => {
    const closeButton = useRef(null)
    const [availablePropertyTypes, setAvailablePropertyTypes] = useState([
        {id: ''}
    ])
    
    const [formData, setFormData] = useState({
        min_investment: 0,
        max_investment: 0,
        target_roi: 0,
        preferred_hold_period: 1,
        wants_dividend_reinvestment: false,
        investment_goals: '',
        alert_on_new_properties: false,
        preferred_property_types: '',
    })


    const getPropertyTypes = async () => {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/property/api/v1/property-types/`, 
        {
            cache: 'no-store'
        }
    );
    if (res.status === 200){
        const data = await res.json()
        setAvailablePropertyTypes(data);
        console.log(data)
    }

    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const {name, value} = e.target

        if (name === "alert_on_new_properties"){
            value === "0" ? 
            setFormData({
                ...formData, [name]: true
            })
            :
            setFormData({
                ...formData, [name]: false
            })
        } else if (name === "wants_dividend_reinvestment"){
            value === "0" ? 
            setFormData({
                ...formData, [name]: false
            })
            :
            setFormData({
                ...formData, [name]: true
            })
        } 
        else{
            setFormData({
            ...formData, 
            [name]: value
        })
        }
    }

    const handleSubmit = async (e: React.FormEvent) => {
        const fullData = {
            ...formData
        }
        
        console.log("Full data here",fullData)

        const CreateInvestorProfileResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/core/api/v1/investor-profiles/`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(fullData)
        });
        if (!CreateInvestorProfileResponse.ok){
            console.log(CreateInvestorProfileResponse.json());
            return;
        }
        if (CreateInvestorProfileResponse.status === 201){
            alert(`${CreateInvestorProfileResponse.json()}`)
            return;
        }
    }


    useEffect(() => {
        console.log("Use effect active")
        getPropertyTypes()
    }, [])

    return (
        <Modal setModalOpen={setModalOpen} title="Complete the form to create your investor profile">
            <div className="flex w-[95%]">
                <div className="flex flex-col gap-2 w-1/2">
                    <div className="flex flex-col gap-1">
                        <p>Preferred property type: </p>
                        <select name="preferred_property_types" onChange={handleChange}
                        className="w-[75%] rounded text-md border-1 border-gray-400">
                            <option value="">----</option>
                            {availablePropertyTypes.map((availablePropertyType) => (
                                <option key={availablePropertyType.id} value={availablePropertyType.id}>{availablePropertyType.category}</option>
                            ))
                            }
                            
                        </select>
                        
                    </div>
                    <div className="flex flex-col gap-1">
                        <p>Minimum Investment: </p>
                        <input type="text" value={formData.min_investment} onChange={handleChange}
                        name="min_investment" id="min_investment" className="w-[75%] rounded text-xl border-1 border-gray-400" />
                    </div>
                    <div className="flex flex-col gap-1">
                        <p>Maximum Investment: </p>
                        <input type="text" value={formData.max_investment} onChange={handleChange}
                        name="max_investment" id="max_investment" className="w-[75%] rounded text-xl border-1 border-gray-400" />
                    </div>
                    <div className="flex flex-col gap-1">
                        <p>Target ROI: </p>
                        <input type="text" value={formData.target_roi} onChange={handleChange}
                        name="target_roi" id="target_roi" className="w-[75%] rounded text-xl border-1 border-gray-400" />
                    </div>
                    <div className="flex flex-col gap-1">
                        <p>Minimum Investment Period: </p>
                        <input type="text" value={formData.preferred_hold_period} onChange={handleChange}
                        name="preferred_hold_period" id="preferred_hold_period" className="w-[75%] rounded text-xl border-1 border-gray-400" />
                    </div>
                </div>

                <div className="flex flex-col gap-2 w-1/2">
                <div className="flex flex-col gap-1">
                    <p>Do you want your dividends to be re-invested?: </p>
                    <div>
                    <div>
                        <input type="radio" onChange={handleChange} value={1}
                        name="wants_dividend_reinvestment" id="yes" className="me-2" />
                        <span>Yes</span>
                    </div>

                    <div>
                        <input type="radio"  onChange={handleChange} value={0}
                        name="wants_dividend_reinvestment" id="no" className="me-2" />
                        <span>No</span>
                    </div>
                    </div>
                </div>
                <div>
                    <p>What are your investment goals?</p>
                    <textarea value={formData.investment_goals} onChange={handleChange}
                    name="investment_goals" id="investment_goals" className="rounded border-1 border-gray-400 w-[75%]"></textarea>
                </div>
                <div className="flex flex-col items-start">
                    <p>Alert on new properties: </p>
                    <div className="flex gap-2">
                    <input type="checkbox" value={formData.alert_on_new_properties==false ? 0 : 1} checked={!!formData.alert_on_new_properties} onChange={handleChange}
                    name="alert_on_new_properties" id="alert_on_new_properties" />
                    <span>I want to receive alert on new properties</span>
                    </div>
                    
                </div>
                </div>
            </div>
            <div>
                <button
                    onClick={handleSubmit}
                    className="bg-blue-500 text-white px-2 py-1 rounded">{submitText}</button>
            </div>
        </Modal>

    )
}

export default CreateInvestorProfile;