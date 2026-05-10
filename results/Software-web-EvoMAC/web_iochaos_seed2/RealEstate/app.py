




stylesheet RealEstate web
Provides consistent responsive
*/


* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

{
    font-family: Arial, Helvetica, sans-serif;
    background-color: #f9f9f9;
    color: #333;
    line-height: 1.6;
    padding: 20px;
}

Container */
#dashboard-page,


#inquiry-page,



{
    max-width: 1200px;
    margin: 0 auto;
    background-color: #fff;
    padding: 20px 30px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

Headings */
{
    font-size: 2.5rem;
    margin-bottom: 20px;
    color: #2c3e50;
}

{
    font-size: 1.8rem;
    margin-bottom: 15px;
    color: #34495e;
}

{
    font-size: 1.3rem;
    margin-bottom: 10px;
    color: #2c3e50;
}

*/
button {
    background-color: #2980b9;
    color: white;
    border: none;
    padding: 10px 18px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s ease;
}


{
    background-color: #1c5980;
    outline: none;
}

/*


#favorites-page

#locations-page {
    margin-top: 25px;
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
}

Property cards
{
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

*/
{
    background-color: #ecf0f1;
    border-radius: 8px;
    padding: 15px 20px;
    width: 300px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

{
    margin-bottom: 8px;
}

.property-card p {
    margin-bottom: 6px;
    font-size: 0.95rem;
}

*/
{
    margin-top: 10px;
}

Input fields and



input[type="number"],
select,
{
    width: 100%;
    padding: 8px 10px;
    margin-bottom: 15px;
    border: 1px solid #bdc3c7;
    border-radius: 5px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}


input[type="email"]:focus,
input[type="tel"]:focus,


textarea:focus {
    border-color: #2980b9;
    outline: none;
}


{
    resize: vertical;
    min-height: 100px;
}

Tables
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
}

{
    padding: 12px 15px;
    border: 1px solid #ddd;
    text-align: left;
    font-size: 0.95rem;
}

{
    background-color: #2980b9;
    color: white;
}

{
    background-color: #f2f2f2;
}

IDs specific

Featured properties
#featured-properties {
    margin-bottom: 40px;
}

/*
{
    margin-bottom: 40px;
}

Properties
#properties-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}


#favorites-list {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

Agents
#agents-list {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}


.agent-card {
    background-color: #ecf0f1;
    border-radius: 8px;
    padding: 15px 20px;
    width: 280px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

{
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 12px;
}

*/
{
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}


.location-card {
    background-color: #ecf0f1;
    border-radius: 8px;
    padding: 15px 20px;
    width: 300px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

/* message */
{
    color: #e74c3c;
    font-weight: bold;
    margin-bottom: 15px;
}

*/
{
    .property-cards,
    #properties-grid,
    #favorites-list,
    #agents-list,
    #locations-list {
        flex-direction: column;
        align-items: center;
    }

.property-card,
.agent-card,
{
        width: 90%;
    }

{
        flex-direction: column;
    }
}

