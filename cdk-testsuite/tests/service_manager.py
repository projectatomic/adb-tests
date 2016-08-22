#!/usr/bin/python

from avocado import Test
from avocado import main
from avocado.utils import process
import re, os, imp, vagrant, pexpect, re ,time
import subprocess
vsm = imp.load_source('vsm', '../Logic/vsm.py')


class service_manager(Test):
	def setUp(self):
		self.log.info("setup")
		self.vagrant_BOX_PATH=self.params.get('vagrant_BOX_PATH')
		self.vagrant_PLUGIN_PATH=self.params.get('vagrant_PLUGIN_PATH')	
		self.service = self.params.get('service', default='')
		self.vagrant_PROVIDER = self.params.get('vagrant_PROVIDER', default='hyperv')
		os.chdir(self.vagrant_BOX_PATH)
		self.v = vagrant.Vagrant(self.vagrant_BOX_PATH)

	def est_cdkbox_version(self):
		self.log.info(os.system("pwd"))
		output = vsm.vsm_box_info(self.vagrant_BOX_PATH, "version", "--script-readable")
		self.log.info(output)
		print output
		if "Container Development Kit (CDK)" in output.stdout:
			pass

		else:
			self.assertEquals("Container Development Kit(CDK)",output.stdout)
	def  est_vsm_box_ip(self):
		output = vsm.vsm_box_info(self.vagrant_BOX_PATH, "ip", "")
		ip = output.stdout
		ips = re.findall('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})',ip)
		print ips[0]
		if ips[0] != None:
			pass
		else: 
			self.assertTrue(False)
		
	def est_env_info_docker(self):

		output = vsm.vsm_env_info(self.vagrant_BOX_PATH, "docker","--script-readable")
		print output.stdout
		if "DOCKER_HOST" and "DOCKER_CERT_PATH" and "DOCKER_TLS_VERIFY" and "DOCKER_API_VERSION" in output.stdout:
			print "Test pass"
			pass
		else:
			self.assertTrue(False)


	def est_env_info_openshift(self):
		output = vsm.vsm_env_info(self.vagrant_BOX_PATH, "openshift","--script-readable")
		print output.stdout
		if "OPENSHIFT_URL" and "OPENSHIFT_WEB_CONSOLE" and "DOCKER_REGISTRY"  in output.stdout:
			print "Test pass"
			pass
		else:
			self.assertTrue(False)

	def est_vsm_status_of_docker_service_running(self):
		output = vsm.vsm_service_handling(self.vagrant_BOX_PATH, "status", "docker")
		print output.stdout
		if "docker - running" in output.stdout:
			pass
		else:
			self.assertTrue(False)

	def est_vsm_status_openshift_service_running(self):
		output = vsm.vsm_service_handling(self.vagrant_BOX_PATH, "status", "openshift")
		print output.stdout
		if "openshift - running" in output.stdout:
			pass
		else:
			self.assertTrue(False)
	
	def est_stop_openshift_service_start_again(self):
		vsm.vsm_service_handling(self.vagrant_BOX_PATH, "stop", "openshift")
		output = vsm.vsm_service_handling(self.vagrant_BOX_PATH, "status", "openshift")
		print output.stdout
		if "openshift - stopped" in output.stdout:
			restart = vsm.vsm_service_handling(self.vagrant_BOX_PATH, "start", "openshift")
			output = vsm.vsm_service_handling(self.vagrant_BOX_PATH, "status", "openshift")
		
			time.sleep(20)
			if "openshift - running" in output.stdout:
				pass
			else:
				self.assertTrue(False)
			pass
		else:
			self.assertTrue(False)
		
	def est_stop_docker_service_start_again(self):
		vsm.vsm_service_handling(self.vagrant_BOX_PATH, "stop", "docker")
		output = vsm.vsm_service_handling(self.vagrant_BOX_PATH, "status", "docker")
		print output.stdout
		if "docker - stopped" in output.stdout:
			restart = vsm.vsm_service_handling(self.vagrant_BOX_PATH, "start", "docker")
			output = vsm.vsm_service_handling(self.vagrant_BOX_PATH, "status", "")
		
			time.sleep(20)
			if "docker - running" and "openshift - running" in output.stdout:
				pass
			else:
				restart = vsm.vsm_service_handling(self.vagrant_BOX_PATH, "restart", "docker")
				output = vsm.vsm_service_handling(self.vagrant_BOX_PATH, "status", "")
				time.sleep(30)
				if "docker - running" and "openshift - running" in output.stdout:
					pass
				else:

					self.assertTrue(False)
			pass
		else:
			self.assertTrue(False)
		

   	

   	def est_docker_version_host(self):
   		(out,err)=vsm.instll_cli(self.vagrant_BOX_PATH, "docker", "docker version")
   		print out,err
   		if 'Client' and 'Server' in out:
   			pass
   		else:
   			self.assertTrue(False)
   		

   	def est_docker_images_host(self):
   		(out,err)=vsm.instll_cli(self.vagrant_BOX_PATH, "docker", "docker images")
   		print out,err
   		if 'registry.access.redhat.com' in out:
   			pass
   		else:
   			self.assertTrue(False)

   	def est_docker_ps(self):
   		(out,err)=vsm.instll_cli(self.vagrant_BOX_PATH, "docker", "docker ps")
   		print out,err
   		if 'openshift' in out:
   			pass
   		else:
   			self.assertTrue(False)
   	def est_docker_pull(self):
   		(out,err)=vsm.instll_cli(self.vagrant_BOX_PATH, "docker", "docker pull tutum/hello-world")
   		print out,err
   		if 'Status: Downloaded newer image for docker.io/tutum/hello-world:latest' in out:
   			pass
   		else:
   			self.assertTrue(False)
   	
   	
   	def est_docker_rmi(self):
   		(out,err)=vsm.instll_cli(self.vagrant_BOX_PATH, "docker", "docker rmi tutum/hello-world")
   		print out,err
   		if 'Deleted' in out:
   			pass
   		else:
   			self.assertTrue(False)


   	def est_openshift_from_host_version(self):

   		(out,err)=vsm.instll_cli(self.vagrant_BOX_PATH, "openshift", "oc version")
   		print out,err
   		if 'oc v1.2.1' in out:
   			pass
   		else:
   			self.assertTrue(False)
   	def est_openshift_from_host_version(self):

   		(out,err)=vsm.instll_cli(self.vagrant_BOX_PATH, "openshift", "oc version")
   		print out,err
   		if 'oc v1.2.1' in out:
   			pass
   		else:
   			self.assertTrue(False)
   		
   	def est_openshift_login_host(self):
   		(out,err)=vsm.box_ip(self.vagrant_BOX_PATH,'ip')
   		out=out.replace('ESC[0m','')
   		ips = re.findall('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})',out)
		print ips[0]
   		(out,err)=vsm.instll_cli(self.vagrant_BOX_PATH, "openshift", "oc login " +ips[0]+" --username=openshift-dev "+" --password=devel  --insecure-skip-tls-verify")
   		print out,err
   		
   		if 'Login successful' in out:
   			pass

   		else:
   			self.assertTrue(False)
   		
   		
   	
   	def test_openshift_newproject_host(self):
   		(out,err)=vsm.box_ip(self.vagrant_BOX_PATH,'ip')
   		out=out.replace('ESC[0m','')
   		ips = re.findall('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})',out)
		print ips[0]
   		(out,err)=vsm.instll_cli(self.vagrant_BOX_PATH, "openshift", "oc login " +ips[0]+" --username=openshift-dev "+" --password=devel  --insecure-skip-tls-verify;oc new-project test-project")
   		print out,err
		   		
   		if 'test-project' in out:
   			pass

   		else:
   			self.assertTrue(False)
   		