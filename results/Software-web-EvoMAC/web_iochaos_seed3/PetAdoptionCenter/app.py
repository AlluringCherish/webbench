


lang="en">


<title>Pet

/* for layout
{
            font-family: Arial, sans-serif;
            margin: 20px;
        }
{
            max-width: 1000px;
            margin: 0 auto;
        }
{
            text-align: center;
        }
{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 30px;
        }
{
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 10px;
            width: 180px;
            box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
img {
            width: 160px;
            height: 120px;
            object-fit: cover;
            border-radius: 4px;
            margin-bottom: 8px;
        }
.pet-name {
            font-weight: bold;
            margin-bottom: 4px;
        }
.pet-species-age {
            font-size: 0.9em;
            color: #555;
            margin-bottom: 8px;
        }
#recent-activities {
            margin-bottom: 30px;
        }
h2 {
            margin-bottom: 10px;
        }
{
            list-style: none;
            padding-left: 0;
        }
{
            margin-bottom: 6px;
            border-bottom: 1px solid #eee;
            padding-bottom: 6px;
        }
button {
            padding: 10px 20px;
            margin-right: 10px;
            border: none;
            background-color: #007BFF;
            color: white;
            border-radius: 4px;
            cursor: pointer;
            font-size: 1em;
        }
{
            background-color: #0056b3;
        }
{
            text-align: center;
            margin-bottom: 30px;
        }
{
            color: #007BFF;
            text-decoration: none;
        }
a.pet-link:hover {
            text-decoration: underline;
        }




Adoption
id="featured-pets">

{% if featured_pets %}
{% for pet in featured_pets %}

<a href="{{ url_for('pet_details', pet_id=pet.pet_id) }}"
image, be
onerror="this.onerror=null;this.src='{{ url_for('static', filename='images/pets/default.jpg') }}';">
id="pet-name-{{ pet.pet_id }}">{{ pet.name }}</div>
<div id="pet-species-age-{{ pet.pet_id }}">{{ pet.species }}, {{ pet.age }}</div>

</div>
{% endfor %}
{% else %}
<p>No moment.</p>
{% endif %}

<section


{% if recent_applications %}

{% for app in recent_applications %}


{% set pet = pet_dict.get(app.pet_id) %}
{% if pet %}

{% else %}

{% endif %}

{{ app.status }}<br>
{{ app.date_submitted }}
</li>
{% endfor %}
</ul>
{% else %}
<p>You
{% endif %}
</section>


<button
</div>
</div>
</body>

