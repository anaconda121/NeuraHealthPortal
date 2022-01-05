# Navigating the ``Davidson`` Folder
1. ``migrations/`` - Auto generated folder that would usually hold files that represent the edits to a database during the course of project. There was no database used for this project as it is unethical to store sensitive patient EHR notes. 
2. ``static/`` - Houses all CSS/JS/ image assets
	* ``css/`` - All CSS stylesheets used for the portal. All of these were generated from the web template mentioned in root ``README.md``. 
	* ``images/`` - All image files used for the portal. All of them with the exception of ``scatter_plot.png`` were found on the internet and approximately credited on the portal frontend.  
	* ``js/`` - All javascript scripts used for the portal. All of them with the exception of ``predict.js`` were generated from the aforementioned template. 
3. ``templates/gui/`` - Houses all HTML/PHP template files. Initially generated from the web template and then further iterated on by me.   
4. ``__init__.py`` - Django Auto generated config file.
5. ``{patient_level_model, run_clinical_bert, run_model, sequence_extraction_pipeline, views}.py``  - Backend code that runs and generates model predictions, written by me.
6. ``urls.py`` - Django Auto generated config file that was further iterated on by me. 
