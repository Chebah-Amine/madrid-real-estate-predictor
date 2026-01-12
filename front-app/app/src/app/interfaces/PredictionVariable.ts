export interface PredictionVariable {
    label: string // le titre du bail
    type : "string"|"number"|"boolean" // le type du bail 
    value: string|number|boolean // la valeur à récupérer dans le formulaire
    defaults?:any // les valeurs par défaut (si c'est un select-options par exemple)
}